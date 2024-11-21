# config1
<h1 align="center">Домашняя работа №1 - Эмулятор для языка оболочки ОС</a> 
<h3 align="center">Постановка задачи</h3>
  
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
tar. Эмулятор должен работать в режиме GUI.

Ключами командной строки задаются:

• Имя пользователя для показа в приглашении к вводу.

• Путь к архиву виртуальной файловой системы.

• Путь к лог-файлу.

• Путь к стартовому скрипту.

Лог-файл имеет формат xml и содержит все действия во время последнего
сеанса работы с эмулятором. Для каждого действия указан пользователь.
Стартовый скрипт служит для начального выполнения заданного списка
команд из файла.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:

1. touch.
2. date.

Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 2 теста.

### Запуск программы
```bash
cd config\emulator var26\emulator var26
.venv\Scripts\activate
python emulator.py --user test_user --tar virtual_file_system.tar --log log.xml --script startup_script.sh
```


### Скрины работы программы
- Комманда ``ls``
  
![image](https://github.com/user-attachments/assets/0b6c3c56-b466-4332-8f07-937806bb0c1a)



- Комманда ``cd``

![image](https://github.com/user-attachments/assets/3b5f1243-ac0b-4fe1-a110-9540963df162)



- Комманда ``date``

![image](https://github.com/user-attachments/assets/87253ac6-209f-4662-8815-c070ba416c5c)



- Комманда ``touch``

![image](https://github.com/user-attachments/assets/7db1a20c-5f08-4be6-a01a-e25b7c20a9ef)



- Комманда ``exit``

![image](https://github.com/user-attachments/assets/36ce3e15-3e37-48a8-acae-b7846d66781e)



### Результаты тестов

![image](https://github.com/user-attachments/assets/c6a9cc05-af4b-41f4-8b53-41e93f4de6ac)


### Логи

![image](https://github.com/user-attachments/assets/6dc079c5-2b07-4c63-b8d7-5d75a91b1d04)

