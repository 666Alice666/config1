import pytest
from emulator import ShellEmulator


# Фикстура для создания виртуальной файловой системы
@pytest.fixture
def mock_filesystem():
    return {
        '': None,
        'folder1': None,
        'folder1/file1.txt': b'file 1',
        'folder1/file2.txt': b'file 2',
        'folder1/file3.txt': b'file 3',
        'folder2': None
    }


# Фикстура для создания экземпляра ShellEmulator
@pytest.fixture
def shell(mock_filesystem):
    return ShellEmulator("test-host", "/", mock_filesystem)


# Тесты для команды cd
def test_cd_success(shell):
    result = shell.cd("/folder1")  # Абсолютный путь
    assert shell.current_dir == "folder1", "Переход в каталог должен быть успешным."
    assert result == "Changed directory to folder1", "Сообщение должно подтверждать успешный переход."


def test_cd_nonexistent(shell):
    result = shell.cd("/nonexistent")
    assert result == "No such directory: /nonexistent", "Должна быть ошибка для несуществующего каталога."


# Тесты для команды ls
def test_ls_success(shell):
    result = shell.ls("/folder1")  # Указываем корневой каталог
    assert result == ['file1.txt', 'file2.txt', 'file3.txt'], "Команда ls должна возвращать содержимое каталога folder1."


def test_ls_nonexistent(shell):
    result = shell.ls("nonexistent")
    assert result == ["No such directory: nonexistent"], "Должна быть ошибка для несуществующего каталога."


# Тесты для команды touch
def test_touch_success(shell):
    result = shell.touch("newfile.txt")
    assert result == "File 'newfile.txt' created in /", "Файл должен быть успешно создан."
    assert "/newfile.txt" in shell.filesystem, "Файл должен существовать в виртуальной файловой системе."


def test_touch_existing_file(shell):
    shell.filesystem["/existingfile.txt"] = b""
    result = shell.touch("existingfile.txt")
    assert result == "File 'existingfile.txt' already exists.", "Должна быть ошибка для существующего файла."


# Тесты для команды date
def test_date_format(shell):
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = shell.get_date()
    assert result == current_date, "Команда date должна возвращать текущую дату и время."


def test_date_correct_output(shell):
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    result = shell.get_date()
    assert current_date in result, "Команда date должна возвращать текущую дату."
