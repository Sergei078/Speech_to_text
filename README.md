# Speech_to_text(Telegram Bot)
## Описание проекта
Код предназначен для распознование голосового сообщения в телеграм боте. Ваше голосовое сообщение будет обработано 
если оно не превышает 30 секунд, также вам выделено 5 аудио-блоков(счет блоков начинается с 1), также при распознование
голосового, его текст записываеться в базу данных, и считается на символы, все это можно будет узнать если перейти в 
меню и нажать "Баланс". 

## Используемые библиотеки
![PyPI - Version](https://img.shields.io/pypi/v/aiogram?style=flat&label=aiogram&labelColor=red&color=green)<br>
![PyPI - Version](https://img.shields.io/pypi/v/requests?style=flat&label=requests&labelColor=red&color=green)<br>
![PyPI - Version](https://img.shields.io/pypi/v/python-dotenv?label=python-dotenv&labelColor=red&color=green)<br>


## Как запустить проект у себя
Вам нужно иметь версию Pytnon 3.12(Последняя версия). Установить все необходимые библиотеки:<br>
1. Установить aiogram<br>
  ```
  pip install aiogram
  ```
2. Установить requests
  ```
  pip install requests
  ```
3. Установить python-dotenv
 ```
 pip install python-dotenv
 ```
**Дополнительные библиотеки которые есть в проекте, предварительно устанавливать не нужно, их нужно только импортировать.**
## Файл .env
*Создать обычный файл дать название .env*<br>
Здесь вам нужно указать:<br> 
+ TOKEN **(Токен бота)**
+ iam_token 
+ folder_id
+ URL **(Указать адрес для запроса)**
+ file **(Название файла куда будет сохраняться голосовое сообщение, расширение .ogg)**
+ db_file **(Название базы данных расширение .db)**
+ file_error **(Название файла для записывание ошибок)**<br>

**Все константы которые указаны используются в проекте, поэтому их название копируйте отсюда!**