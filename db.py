import sqlite3
from datetime import datetime

class User:
    def __init__(self,tel_id, user_name):
        self.tel_id = tel_id
        self.user_name = user_name
        self.db_connection = self._connect_db()
        self.log_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # automaticaly called during initiation of class
        self._create_db()
        self._insert_user()
        self._load_logtime()
        self.status = self._get_status()


    def _connect_db(self):
        return sqlite3.connect('tasks.db')

    def _create_db(self):
        query_users = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER,
                user_name TEXT,
                status TEXT,
                log_time TEXT
            )
        '''
        self._execute_query(query_users)


    def _execute_query(self, query, params=None):
        conn = self.db_connection
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor

    def _insert_user(self):
        if self.check_db_for_user() == False:
            query = "INSERT INTO users (telegram_id, user_name, status) VALUES (?, ?,?)"
            self._execute_query(query, (self.tel_id, self.user_name,"Start"))
        else:
            pass

    def _load_logtime(self):
        if self.check_db_for_user():
            query = "UPDATE users SET log_time = ? WHERE telegram_id = ?"
        self._execute_query(query, (self.log_time, self.tel_id))




    def check_db_for_user(self):
        query = "SELECT * FROM users WHERE telegram_id = ?"
        pseudo_cursor = self._execute_query(query, (self.tel_id,))
        if pseudo_cursor.fetchone():
            return True
        else:
            return False
        

    def _get_status(self):
        query = "SELECT status FROM users WHERE telegram_id = ?"
        return self._execute_query(query,(self.tel_id,))

    def close_db_connection(self):
        self.db_connection.close()





class Task(User):

    def __init__(self,description,datetime):
        self.description = description
        self.datetime = datetime
        self.db_connection = self._connect_db
        self._create_db()


    def _create_db(self):
        query_tasks = '''
            CREATE TABLE IF NOT EXISTS tasks (
                user_id INTEGER,
                task_id INTEGER,
                task_note TEXT,
                data_time TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        '''
        self._execute_query(query_tasks)


    def _get_last_task_id(self,user_id):
        query = "SELECT MAX(task_id) FROM tasks WHERE user_id = ?"
        cursor = self._execute_query(query, (user_id,))
        result = cursor.fetchone()
        if result[0] is not None:
            return result[0]
        else:
            return 0
        

    def insert_task(self,user_id, task_note, data_time):
        last_task_id = self._get_last_task_id()
        new_task_id = last_task_id + 1
        query = "INSERT INTO tasks (user_id, task_id, task_note, data_time) VALUES (?, ?, ?, ?)"
        self._execute_query(query, (user_id, new_task_id, task_note, data_time))
    
    def get_user_tasks(self,user_id):
        query = "SELECT task_id, task_note, data_time FROM tasks WHERE user_id = ?"
        cursor = self._execute_query(query, (user_id,))
        tasks = cursor.fetchall()
        return tasks
    
    def remove_users_task(self, task_id, user_id):
        query = "DELETE FROM tasks WHERE id = ? AND user_id = ?"
        self._execute_query(query, (task_id, user_id))
        pass    
    


