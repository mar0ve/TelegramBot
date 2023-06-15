import mysql.connector
from datetime import datetime


class ManageDatabase:
    conn = None
    cursor = None

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )

        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()

    def query(self, sql, values=None):
        try:
            #cursor = self.conn.cursor()
            self.cursor.execute(sql, values)
        except (AttributeError, mysql.connector.OperationalError):
            self.connect()
            #cursor = self.conn.cursor()
            self.cursor.execute(sql, values)

    def register_user(self, chat_id, first_name, last_name):
        self.connect()
        sql = "INSERT INTO users (chat_id, first_name, last_name) VALUES (%s, %s, %s)"
        values = (chat_id, first_name, last_name)
        self.query(sql, values)
        self.conn.commit()
        self.disconnect()

    def start_workday(self, user_id):
        self.connect()
        sql = "INSERT INTO work_logs (user_id, start_time) VALUES (%s, %s)"
        values = (user_id, datetime.now())

        self.query(sql, values)
        self.conn.commit()
        self.disconnect()

    def end_workday(self, user_id):
        self.connect()
        sql = "UPDATE work_logs SET end_time = %s WHERE user_id = %s AND end_time IS NULL"
        values = (datetime.now(), user_id)
        self.query(sql, values)
        self.conn.commit()
        self.disconnect()

    def print_info(self, chat_id):
        self.connect()
        sql = """
            SELECT users.first_name, users.last_name, work_logs.start_time, work_logs.end_time
            FROM work_logs
            INNER JOIN users ON work_logs.user_id = users.id
            WHERE users.chat_id = %s
        """
        values = (chat_id,)
        self.query(sql, values)
        work_logs = self.cursor.fetchall()
        self.disconnect()
        return work_logs

    def print_all_info(self):
        self.connect()
        sql = """
            SELECT users.first_name, users.last_name, work_logs.start_time, work_logs.end_time
            FROM users
            LEFT JOIN work_logs ON users.id = work_logs.user_id
        """
        self.query(sql)
        work_logs = self.cursor.fetchall()
        self.disconnect()
        return work_logs

    def check_user(self, chat_id):
        self.connect()
        sql = "SELECT * FROM users WHERE chat_id = %s"
        values = (chat_id,)
        self.query(sql, values)
        user = self.cursor.fetchone()
        self.disconnect()
        return user