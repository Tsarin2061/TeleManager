# here I try to reimplement class DB as it should have looked like
import sqlite3
import logging

class DataBase():
    def __init__(self) -> None:
        self.db_connection = self._connect_db()
        self._create_db()
        pass

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
        query_tasks = '''
            CREATE TABLE IF NOT EXISTS tasks (
                user_id INTEGER,
                task_id INTEGER PRIMARY KEY,
                task_note TEXT,
                data_time TEXT,
                status TEXT,
                collaborators_id INTEGER,
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
        self._execute_query(query_users)
        logging.INFO(f"Created 3 DBs")

    
    def _execute_query(self, query, params=None):
        conn = self.db_connection
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor
    
    def close_db_connection(self):
        self.db_connection.close()