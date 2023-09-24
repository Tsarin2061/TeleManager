import sqlite3
from datetime import datetime
from src.newdb import DataBase

class Task(DataBase):

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

    def add_collaborator(self,colab_id):
        task_id = self.__get_last_task_id()
        query = "UPDATE tasks SET collaborators_id = ? WHERE user_id = ? AND task_id = ?"
        self._execute_query(query,(colab_id,self.user_id,task_id))


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
        query = 'SELECT task_id, task_note, data_time FROM tasks WHERE user_id = ? and status = "active"'
        cursor = self._execute_query(query, (self.user_id,))
        tasks = cursor.fetchall()
        return tasks
    
    def get_collaborators_id(self,task_id):
        query = "SELECT collaborators_id FROM tasks WHERE task_id = ?"
        cursor = self._execute_query(query,(task_id,))
        id = cursor.fetchall()
        return id
    

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

