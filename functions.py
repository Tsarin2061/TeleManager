from datetime import datetime
import sqlite3
from threading import Timer

def extract_date():
    """extracts data from DB 

    Returns:
        dictionary : returns dict with telegram id of user, task notes and date
    """
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    db = sqlite3.connect('tasks.db')
    cursor = db.cursor()

    try:
        get_id = "SELECT telegram_id FROM users WHERE id = (SELECT user_id FROM tasks WHERE data_time = ?)"
        cursor.execute(get_id, (current_time,))
        tel_id = cursor.fetchone()[0]
        # Get the date and task based on the telegram_id and current_time
        get_task = '''SELECT data_time, task_note, task_id
                    FROM tasks WHERE user_id = 
                    (SELECT id FROM users WHERE telegram_id = ?)
                    AND data_time = ? AND status = "active"'''
        cursor.execute(get_task, (tel_id, current_time))
        date, task, task_id = cursor.fetchone()
        return {
        "telegram_id": tel_id,
        "task_id":task_id,
        "date": date,
        "task": task
    }
    except:
        db.commit()
        db.close()

        return False