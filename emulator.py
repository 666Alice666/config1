import os
import tarfile
import time
from logger import Logger
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget

import argparse


def parse_arguments():
    """
    Парсинг аргументов командной строки.
    """
    parser = argparse.ArgumentParser(description="Shell Emulator with GUI")
    parser.add_argument("--user", required=True, help="User name for the prompt")
    parser.add_argument("--tar", required=True, help="Path to the virtual file system archive")
    parser.add_argument("--log", required=True, help="Path to the log file")
    parser.add_argument("--script", required=True, help="Path to the startup script")
    return parser.parse_args()



def extract_filesystem_to_memory(tar_path):
    filesystem = {}
    with tarfile.open(tar_path, 'r') as tar:
        for member in tar.getmembers():
            if member.isfile():
                file_content = tar.extractfile(member).read()
                filesystem[member.name] = file_content
            else:
                filesystem[member.name] = None  # Директория, у которой нет содержимого
    return filesystem

class ShellEmulator:
    def __init__(self, hostname, root_dir, filesystem):
        self.hostname = hostname
        self.current_dir = root_dir
        self.filesystem = filesystem
        self.start_time = time.time()

    def _get_full_path(self, path):
        full_path = self.current_dir + "/" + path
        parts = []
        for part in full_path.split("/"):
            if part == "..":
                if parts:
                    parts.pop()
            elif part and part != ".":
                parts.append(part)
        normalized_path = "/" + "/".join(parts)
        return normalized_path.lstrip("/")

    def cd(self, path):
        new_dir = self._get_full_path(path)
        if new_dir in self.filesystem and self.filesystem[new_dir] is None:
            self.current_dir = new_dir
            return f"Changed directory to {self.current_dir}"
        else:
            return f"No such directory: {path}"

    def ls(self, path=None):
        if path is not None:
            target_dir = self._get_full_path(path)
        else:
            target_dir = self.current_dir.lstrip("/")
        if target_dir in self.filesystem and self.filesystem[target_dir] is None:
            contents = [p[len(target_dir) + 1:].split("/")[0] for p in self.filesystem if p.startswith(target_dir + "/")]
            return list(sorted(set(contents)))
        elif target_dir == "":
            contents = [p.split("/")[0] for p in self.filesystem if "/" in p]
            return list(sorted(set(contents)))
        else:
            return [f"No such directory: {target_dir}"]

    def touch(self, filename):
        """
        Создаёт виртуальный файл в текущем каталоге.
        """
        new_file_path = self.current_dir.rstrip("/") + "/" + filename
        if new_file_path in self.filesystem:
            return f"File '{filename}' already exists."
        self.filesystem[new_file_path] = b""  # Создаём пустой файл
        return f"File '{filename}' created in {self.current_dir}"

    def get_date(self):
        """
        Возвращает текущую дату и время.
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class EmulatorGUI(QMainWindow):
    def __init__(self, username, filesystem, script_path=None, log_path=None):
        super().__init__()
        self.username = username
        self.shell = ShellEmulator(username, "/", filesystem)
        self.logger = Logger(log_path) if log_path else None
        self.initUI()

        # Выполняем скрипт, если путь указан и тесты не выполняются
        if script_path:
            self.run_startup_script(script_path)

    def get_prompt(self):
        """
        Формирует приглашение с именем пользователя и текущим каталогом.
        """
        return f"{self.username}:{self.shell.current_dir}$ "

    def initUI(self):
        """
        Инициализация графического интерфейса.
        """
        self.setWindowTitle("Shell Emulator")
        self.resize(800, 600)

        self.setStyleSheet("""
            QMainWindow {
                background-color: black;
            }
            QTextEdit {
                background-color: black;
                color: green;
                font-family: Consolas;
                font-size: 12pt;
                border: none;
            }
            QLineEdit {
                background-color: black;
                color: green;
                font-family: Consolas;
                font-size: 12pt;
                border: 1px solid green;
            }
        """)

        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)

        self.command_input = QLineEdit(self)
        self.command_input.returnPressed.connect(self.execute_command)

        layout = QVBoxLayout()
        layout.addWidget(self.text_display)
        layout.addWidget(self.command_input)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Приветственное сообщение
        self.display_output(f"Welcome to {self.username} Shell Emulator")

    def execute_command(self):
        command = self.command_input.text().strip()
        if not command:
            return
        self.display_output(f"{self.shell.hostname}:{self.shell.current_dir}$ {command}")
        output = self.run_command(command)
        if output:
            self.display_output(output)
        self.command_input.clear()

    def run_command(self, command):
        """
        Обрабатывает команды пользователя.
        """
        if command.startswith("ls"):
            parts = command.split(maxsplit=1)
            if len(parts) == 1:
                output = "\n".join(self.shell.ls())
            else:
                output = "\n".join(self.shell.ls(parts[1]))
        elif command.startswith("cd"):
            parts = command.split(maxsplit=1)
            if len(parts) > 1:
                output = self.shell.cd(parts[1])
            else:
                output = "Error: 'cd' requires a path."
        elif command.startswith("touch"):
            parts = command.split(maxsplit=1)
            if len(parts) > 1:
                output = self.shell.touch(parts[1])
            else:
                output = "Error: 'touch' requires a filename."
        elif command == "date":
            output = self.shell.get_date()
        elif command == "exit":
            # Логируем команду exit перед закрытием
            self.logger.log_action(self.username, command)
            self.close()
            return None
        else:
            output = f"Unknown command: {command}"

        # Логируем команду
        self.logger.log_action(self.username, command)

        return output

    def display_output(self, text):
        self.text_display.append(text)

    def run_startup_script(self, script_path):
        """
        Выполняет команды из стартового скрипта.
        """
        if not os.path.exists(script_path):
            self.display_output(f"Startup script '{script_path}' not found.")
            return

        try:
            with open(script_path, "r", encoding="utf-8") as script_file:
                commands = script_file.readlines()
                for command in commands:
                    command = command.strip()
                    if command:
                        self.display_output(f"Executing: {command}")
                        # Выполняем команду через run_command (логирование происходит внутри run_command)
                        output = self.run_command(command)
                        if output:
                            self.display_output(output)
        except Exception as e:
            self.display_output(f"Error reading startup script: {str(e)}")


def main():
    import sys
    from PyQt5.QtWidgets import QApplication

    # Парсим аргументы командной строки
    args = parse_arguments()

    # Загружаем файловую систему из архива
    filesystem = extract_filesystem_to_memory(args.tar)

    app = QApplication(sys.argv)
    gui = EmulatorGUI(args.user, filesystem, args.script, args.log)
    gui.show()
    sys.exit(app.exec_())





if __name__ == "__main__":
    main()
