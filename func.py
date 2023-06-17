from config import db_manager


def print_per_logs(chat_id):
    work_logs = db_manager.print_info(chat_id)
    report = "Отчет о пребывании на работе:\n\n"
    for log in work_logs:
        first_name = log[0]
        last_name = log[1]
        start_time = log[2]
        end_time = log[3] if log[3] is not None else "В процессе"
        report += f"Имя: {first_name}\nФамилия: {last_name}\nНачало дня: {start_time}\nКонец дня: {end_time}\n\n"

    return report


def print_all_logs():
    work_logs = db_manager.print_all_info()
    report = "Отчет о пребывании на работе всех сотрудников:\n\n"
    for log in work_logs:
        first_name = log[0]
        last_name = log[1]
        start_time = log[2]
        end_time = log[3] if log[3] is not None else "В процессе"
        report += f"Имя: {first_name}\nФамилия: {last_name}\nНачало дня: {start_time}\nКонец дня: {end_time}\n\n"

    return report


def set_department_logs(users):
    report = 'Отчет о сотрудниках отдела: \n'

    for usr in users:
        first_name, last_name, email, phone, usr_state = usr
        report += f'Имя и Фамилия: {first_name} {last_name}\nEmail: {email}\nТелефон: {phone}\nСтатус: {usr_state}\n'

    return report
