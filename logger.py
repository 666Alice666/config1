import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import os


class Logger:
    def __init__(self, log_path):
        self.log_path = log_path
        self.clear_log_file()  # Очищаем лог-файл при запуске

    def clear_log_file(self):
        """
        Очищает содержимое лог-файла и инициализирует его как пустой XML.
        """
        try:
            print(f"Clearing log file: {self.log_path}")
            root = ET.Element("log")  # Создаём корневой элемент <log>
            tree = ET.ElementTree(root)
            with open(self.log_path, "wb") as f:
                tree.write(f)
        except Exception as e:
            print(f"Error clearing log file: {str(e)}")

    def log_action(self, user, command):
        """
        Логирует выполненную команду.
        """
        try:
            # Загружаем существующий лог
            tree = ET.parse(self.log_path)
            root = tree.getroot()

            # Создаём новый элемент <action>
            action = ET.Element("action")
            action.set("user", user)
            action.set("time", datetime.now().isoformat())
            action.set("command", command)

            # Добавляем элемент в корневой <log>
            root.append(action)

            # Сохраняем изменения в XML-файл с красивым форматированием
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            with open(self.log_path, "w", encoding="utf-8") as f:
                f.write(xml_str)
        except Exception as e:
            print(f"Error logging action: {str(e)}")

