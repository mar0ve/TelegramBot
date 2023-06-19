# TelegramBot 
Бот предназначен для учета рабочего времени сотрудников компании. 

Для запуска необходим MySQL сервер с созданной БД **telegram_bot**.

MySQL:

``` sql
-- Создание БД telegram_bot
CREATE DATABASE IF NOT EXISTS telegram_bot;
USE telegram_bot;
-- Создание таблицы users
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    chat_id INT,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255),
    reg_date DATETIME,
    use_state VARCHAR(255),
    department VARCHAR(255)
);

-- Создание таблицы work_logs
CREATE TABLE IF NOT EXISTS work_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    start_time DATETIME,
    end_time DATETIME
);
```
Создать файл **.env** и вписать в него строку:
  > TOKEN = "your_telegram_token"

В файле **config.py** изменить db_connection данные на свои

Для быстрой установки всех пакетов
  > pip install -r requirements.txt

Старт:
  > python bot_io.py

## Управление
Для начала нужно нажать кнопку **Начать**

### Этап регистрации:
- Ввести Имя и Фамилию.
  > в формате: имя фамилия через пробел
- Ввести номер телефона.
- Ввести имейл.
- Выбрать отдел, в котором работает сотрудник

### Основное управление
- Начать рабочий день
- Закончить рабочий день
- Отчет
- Полный отчет 
  > доступен только тогда, когда статус пользователя admin
- Профиль сотрудника
  > данные о профиле текущего пользователя
- Редактировать профиль
  > можно отредактировать текущее имя, фамилию, имейл, телефон
- Информация о сотрудниках
  > нужно выбрать отдел из всплывающего меню, выдает информацию обо всех сотрудниках отдела

