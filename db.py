import sqlite3
from datetime import datetime


class User:
    def __init__(self, tel_id, user_name):
        self.tel_id = tel_id
        self.user_name = user_name
        self.db_connection = self._connect_db()
        self.log_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        self._create_db()
        self.__insert_user()
        self.status = self.__get_status()


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

    def __insert_user(self):
        if self.check_db_for_user() == False:
            query = "INSERT INTO users (telegram_id, user_name, status) VALUES (?, ?,?)"
            self._execute_query(query, (self.tel_id, self.user_name,"Start"))
        else:
            pass


    def check_db_for_user(self):
        query = "SELECT * FROM users WHERE telegram_id = ?"
        pseudo_cursor = self._execute_query(query, (self.tel_id,))
        if pseudo_cursor.fetchone():
            return True
        else:
            return False
        

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

    def close_db_connection(self):
        self.db_connection.close()





class Task(User):

    def __init__(self,tel_id):
        self.db_connection = self._connect_db()
        self._create_db()
        # self.status = self.__get_status()
        self.user_id = self.__load_id(tel_id)


    def add_description(self, description):
        query = 'INSERT INTO tasks (task_note, user_id,status) VALUES (?,?,?)'
        self._execute_query(query, (description,self.user_id,"active"))
    

    def add_deadline(self,deadline):
        task_id = self.__get_last_task_id()
        query = "UPDATE tasks SET data_time = ? WHERE user_id = ? AND task_id = ?"
        self._execute_query(query,(deadline,self.user_id,task_id))


    def __load_id(self,id):
        """Converts telegram_id into id in DB

        Args:
            id (int): Telegram id

        Returns:
           0 : no results
                OR
           id : id in DB
        """
        query = "SELECT id FROM users WHERE telegram_id = ?"
        ID = self._execute_query(query, (id,))
        result = ID.fetchone()
        if result[0] is not None:
            return result[0]
        else:
            return 0
    

    def _load_description(self):
        query = "SELECT "
        try:
            pass
        except:
            pass

    def _create_db(self):
        query_tasks = '''
            CREATE TABLE IF NOT EXISTS tasks (
                user_id INTEGER,
                task_id INTEGER PRIMARY KEY,
                task_note TEXT,
                data_time TEXT,
                status TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        '''
        query_editor_tasks = '''
            CREATE TABLE IF NOT EXISTS task_editor (
                editor_id INTEGER,
                to_edit_id INTEGER,
                FOREIGN KEY (editor_id) REFERENCES users (id),
                FOREIGN KEY (to_edit_id) REFERENCES users (id)
            );
        '''
        self._execute_query(query_editor_tasks)
        self._execute_query(query_tasks)


    def __get_last_task_id(self):
        """Evaluate the last task_id added by user.

        Returns:
            int : the last task_id
        """
        query = "SELECT MAX(task_id) FROM tasks WHERE user_id = ?"
        cursor = self._execute_query(query, (int(self.user_id),))
        result = cursor.fetchone()
        if result[0] is not None:
            return result[0]
        else:
            return 0
    
    def get_users_task(self):
        query = "SELECT task_id, task_note, data_time FROM tasks WHERE user_id = ?"
        cursor = self._execute_query(query, (self.user_id,))
        tasks = cursor.fetchall()
        return tasks
    
    def remove_users_task(self, task_id):
        query = "DELETE FROM tasks WHERE task_id = ? AND user_id = ?"
        self._execute_query(query, (task_id, self.user_id))
        pass    

    def update_deadline(self,task_id,new_date):
        query = "UPDATE tasks SET data_time = ? WHERE user_id = ? AND task_id = ?"
        self._execute_query(query,(new_date,self.user_id,task_id))
        pass

    def update_description(self,task_id,new_description):
        query = "UPDATE tasks SET task_note = ? WHERE user_id = ? AND task_id = ?"
        self._execute_query(query,(new_description,self.user_id,task_id))
        pass

    def update_status(self,task_id,new_status):
        query = "UPDATE tasks SET status = ? WHERE user_id = ? AND task_id = ?"

        self._execute_query(query,(new_status,self.user_id,task_id))
        pass

    

        


