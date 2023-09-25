import sqlite3
from datetime import datetime
from src.newdb import DataBase

class User(DataBase):
    def __init__(self, tel_id, user_name):
        self.tel_id = tel_id
        self.user_name = user_name
        self.db_connection = self._connect_db()
        self.log_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        self._create_db()
        self.__insert_user()
        self.status = self.__get_status()
        self.id = self.__get_id_from_db()

    def __insert_user(self):
        if self.check_user_in_db('telegram_id', self.tel_id) == False:
            query = "INSERT INTO users (telegram_id, user_name, status,log_time) VALUES (?,?,?,?)"
            self._execute_query(query, (self.tel_id, self.user_name,"Start",self.log_time))
        else:
            pass

    def __get_id_from_db(self):
        query = "SELECT id FROM users WHERE telegram_id = ?"
        id = self._execute_query(query,(self.tel_id,))
        id_user = id.fetchone()
        if id_user:
            return id_user[0]


    def check_user_in_db(self, field, value):
        if field == 'telegram_id':
            query = "SELECT * FROM users WHERE telegram_id = ?"
        elif field == 'user_name':
            query = "SELECT * FROM users WHERE user_name = ?"
        else:
            raise ValueError("Invalid field name")

        pseudo_cursor = self._execute_query(query, (value,))
        return pseudo_cursor.fetchone() is not None       

    def __get_status(self):
        query = "SELECT status FROM users WHERE telegram_id = ?"
        status = self._execute_query(query,(self.tel_id,))
        row = status.fetchone()
        # Check if a result was found
        if row:
            status = row[0]  # Get the value from the first column (status)
            return str(status)  # Convert status to a string and return it
        else:
            return None 
    
    def change_status(self,status):
        query = "UPDATE users SET status = ? WHERE telegram_id = ?"
        query_log_time = "UPDATE users SET log_time = ? WHERE telegram_id = ?"
        self._execute_query(query,(status,self.tel_id))
        self._execute_query(query_log_time,(self.log_time,self.tel_id))

    def mark_edit_task(self,id_task):
        query = "INSERT INTO task_editor (editor_id, to_edit_id) VALUES(?, ?)"
        self._execute_query(query,(self.id,id_task))

    def pop_task(self):
        query = "SELECT to_edit_id FROM task_editor WHERE editor_id = ?"
        id = self._execute_query(query,(self.id,))
        check = id.fetchone()
        query2 = "DELETE FROM task_editor WHERE editor_id = ?"
        if check:
            reuslts = check[0]
            self._execute_query(query2,(self.id,))
            return str(reuslts)

    def close_db_connection(self):
        self.db_connection.close()
