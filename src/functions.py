from datetime import datetime,timedelta
import sqlite3
import re
import logging

def extract_date():
    logging.debug("Extracting function entered")
    """extracts data from DB 

    Returns:
        dictionary : returns dict with telegram id of user, task notes and date
    """
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    db = sqlite3.connect('tasks.db')
    cursor = db.cursor()

    try:
        get_id = 'SELECT telegram_id, user_name FROM users WHERE id = (SELECT user_id FROM tasks WHERE data_time = ? and status = "active" LIMIT 1)'
        
        cursor.execute(get_id, (current_time,))
        tel_id,tel_user_name= cursor.fetchone()[0:2]

        
        # Get the date and task based on the telegram_id and current_time
        get_task = '''SELECT data_time, task_note, task_id, collaborators_id
                    FROM tasks WHERE user_id = 
                    (SELECT id FROM users WHERE telegram_id = ?)
                    AND data_time = ? AND status = "active"'''
        cursor.execute(get_task, (tel_id, current_time,))

        date, task, task_id, collaborators_username = cursor.fetchone()[0:5]

        get_user_id = '''SELECT telegram_id FROM users WHERE user_name = ?'''
        list_coll = []
        if type(collaborators_username.split(',')) == list:
            for name in collaborators_username.split(','):
                cursor.execute(get_user_id,(name,))
                collaborators_id = cursor.fetchone()[0]
                list_coll.append(collaborators_id)
        else:
            cursor.execute(get_user_id,(collaborators_username,))
            collaborators_id = cursor.fetchone()[0]
            list_coll.append(collaborators_id)
        return {
        "user_name": tel_user_name,
        "telegram_id": tel_id,
        "task_id":task_id,
        "date": date,
        "task": task,
        "collaborator_id":list_coll
    }
    except Exception as e:
        logging.error(f"Ecountered an error {e}")
        return False
# def extract_date():
#     """extracts data from DB 

#     Returns:
#         dictionary : returns dict with telegram id of user, task notes and date
#     """
#     current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
#     db = sqlite3.connect('tasks.db')
#     cursor = db.cursor()

#     try:
#         query = 'SELECT users.telegram_id, users.user_name, tasks.task_id, tasks.task_note, tasks.data_time, tasks.collaborators_id FROM tasks JOIN users ON tasks.user_id=users.id WHERE tasks.data_time = ? AND tasks.status = "active" LIMIT 1;'
#         cursor.execute(query, (current_time,))
#         tel_id, tel_user_name, task_id, task, date, collaborators_username = cursor.fetchone()
#         query = f'SELECT id FROM users WHERE user_name IN ({collaborators_username});'
#         cursor.execute(query)
#         list_coll = [item[0] for item in cursor.fetchall()]
#         return {
#         "user_name": tel_user_name,
#         "telegram_id": tel_id,
#         "task_id":task_id,
#         "date": date,
#         "task": task,
#         "collaborator_id":list_coll
#     }
#     except Exception as e:
#         return False
    

def process_date(date):
    present_date = datetime.now()
    tomorrow_day = present_date + timedelta(1)

    if re.match(r'\d{2}:\d{2}',date):
        formatted_today = re.sub(r'\d{2}:\d{2}', f"{present_date.strftime('%d/%m/%Y')} {date}", date)
        # Convert the formatted_today string into a datetime object
        formatted_today_datetime = datetime.strptime(formatted_today, "%d/%m/%Y %H:%M")
        # Compare with the current date and time
        if present_date > formatted_today_datetime:
            return re.sub(r'\d{2}:\d{2}', f"{tomorrow_day.strftime('%d/%m/%Y')} {date}", date)
        else: 
            return formatted_today_datetime.strftime("%d/%m/%Y %H:%M")
    elif re.match(r'\d{2}[./\\]\d{2}\s*\d{2}:\d{2}',date):
        date_parts = date.split()
        if len(date_parts) >= 2:
            day = date_parts[0]
            time = date_parts[1]
            date_str = re.sub(r'[./\\]', '/', day)
            formatted_date = f"{date_str}/{present_date.strftime('%Y')} {time}"
            formatted_date_datetime = datetime.strptime(formatted_date,"%d/%m/%Y %H:%M").strftime("%d/%m/%Y %H:%M")
            return formatted_date_datetime
    else:
        return date