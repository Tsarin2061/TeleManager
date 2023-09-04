import sqlite3

class User:
    def __init__(self,tel_id, user_name):
        self.tel_id = tel_id
        self.user_name = user_name
        self.db_connection = self._connect_db()
        self._create_db()


    def _connect_db(self):
        return sqlite3.connect('tasks.db')

    def _create_db(self):
        query_users = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER,
                user_name TEXT
            )
        '''
        query_tasks = '''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                task_id INTEGER,
                task_note TEXT,
                data_time TEXT
            )
        '''
        self._execute_query(query_users)
        self._execute_query(query_tasks)

    def _execute_query(self, query, params=None):
        conn = self.db_connection
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor

    def get_last_task_id(self):
        query = "SELECT MAX(task_id) FROM tasks WHERE user_id = ?"
        cursor = self._execute_query(query, (self.tel_id,))
        result = cursor.fetchone()
        if result[0] is not None:
            return result[0]
        else:
            return 0

    def insert_task(self, task_note, data_time):
        last_task_id = self.get_last_task_id()
        new_task_id = last_task_id + 1
        query = "INSERT INTO tasks (user_id, task_id, task_note, data_time) VALUES (?, ?, ?, ?)"
        self._execute_query(query, (self.tel_id, new_task_id, task_note, data_time))

    def insert_user(self):
        query = "INSERT INTO users (telegram_id, user_name) VALUES (?, ?)"
        self._execute_query(query, (self.tel_id, self.user_name))

    def get_user_tasks(self):
        query = "SELECT task_id, task_note, data_time FROM tasks WHERE user_id = ?"
        cursor = self._execute_query(query, (self.tel_id,))
        tasks = cursor.fetchall()
        return tasks
    
    def remove_users_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = ? AND user_id = ?"
        self._execute_query(query, (task_id, self.tel_id))
        pass

    def close_db_connection(self):
        self.db_connection.close()

class Task():
    pass



# Example usage:
# user1 = User(12345, "John")
# user2 = User(67890, "Alice")

# user1.insert_user()
# user1.insert_task("Task 1", "2023-09-05 10:00:00")
# user1.insert_task("Task 2", "2023-09-06 15:30:00")

# user2.insert_user()
# user2.insert_task("Task 3", "2023-09-07 08:45:00")

# print("User 1's tasks:")
# for task_id, task_note, data_time in user1.get_user_tasks():
#     print(f"Task ID: {task_id}, Task Note: {task_note}, Date and Time: {data_time}")

# print("User 2's tasks:")
# for task_id, task_note, data_time in user2.get_user_tasks():
#     print(f"Task ID: {task_id}, Task Note: {task_note}, Date and Time: {data_time}")

# # Close database connections
# user1.close_db_connection()
# user2.close_db_connection()
