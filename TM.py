from pickle import NONE
from threading import Timer
import telebot
from src.task import Task
from src.user import User
from src.keyboard import main_keyboard, edit_keyboard, collab_question_keyboard
from src.functions import extract_date, process_date


TOKEN = "6601407772:AAG-0XB94Zx3-9Bm69gDVmx9YuJRKDGKzQQ"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start_record(message):
    """Responsible for greating user"""
    User(message.from_user.id, message.from_user.username)
    markup = main_keyboard()
    # greating user
    bot.send_message(
        message.chat.id,
        f"Hi {message.from_user.first_name},\nI was made to help your task managment!",
        reply_markup=markup,
    )


# Define a dictionary to map commands to actions
# New features start from here 
commands = {
    "Add task": ("adding task", "Describe your task.", None),
    "Add collaborators": ("adding collaborators", "Do you want to notify other people?", None),
    "Remove task": ("removing task", "Please provide the task ID for removal.", None),
    "Edit task": ("editing task", "To edit a task, please provide the task ID.", None),
    "Change deadline": (
        "changing deadline",
        "Please provide the new task deadline (e.g., 10/08/2023 22:30)",
        None,
    ),
    "Change description": (
        "changing description",
        "Please generate a new description for your task.",
        None,
    ),
    "Show tasks": ("showing tasks", "Your tasks bip-bip list:", None),
    "Main menu": ("Start", "bip-bip for returning back", main_keyboard()),
}


@bot.message_handler(content_types=["text"])
def handle_message(message):
    """Responsible for responding to user queries"""
    user = User(tel_id=message.from_user.id, user_name=message.from_user.username)
    text = message.text
    task = Task(message.from_user.id)

    if text in commands:
        status, response, markup = commands[text]
        user.change_status(status)
        bot.send_message(message.chat.id, response, reply_markup=markup)

        # in case command could be executed straightforward
        if text == "Show tasks":
            i = 1
            for id_task, note, date in task.get_users_task():
                bot.send_message(
                    message.chat.id, f"№:{i}\nDescription: {note}\nDeadline: {date}"
                )
                i += 1

    # Here we uses subprocesses
    elif user.status == "adding task":
        user.change_status("adding task deadline")
        task.add_description(text)
        bot.send_message(
            message.chat.id,
            "Please provide the task deadline (e.g., 10/08/2023 22:30):",
        )
    elif user.status == "adding task deadline":
        try:
            task.add_deadline(process_date(text))
            bot.send_message(message.chat.id, "Done!\nBip-bip..")
            bot.send_message(message.chat.id, "do want notify a friend?",reply_markup = collab_question_keyboard())
            user.change_status("Start")

        except:
            bot.send_message(message.chat.id, "Provide valid date!")

    elif user.status == "adding collaborator":
        usrname = str(text).replace('@','')
        usrname = usrname.replace(' ', '').strip()
        if user.check_user_in_db("user_name",usrname):
            task.add_collaborator(usrname)
            bot.send_message(message.chat.id, f"{text} will be notified")
            user.change_status("Start")
        else:
            bot.send_message(message.chat.id, f"User {text} is not found")




    elif user.status == "removing task":
        try:
            to_remove = int(text)
        except ValueError:
            bot.send_message(message.chat.id, "Please providea a valid ID!")
        i = 1
        for id_task, note, date in task.get_users_task():
            if i == to_remove:
                task.remove_users_task(id_task)
                bot.send_message(
                    message.chat.id,
                    f"The task #{i} has been successfully removed.\nBip-bip",
                )
            i += 1

        user.change_status("Start")

    elif user.status == "editing task":
        try:
            to_edit = int(text)
            if to_edit:
                user.mark_edit_task(to_edit)
                bot.send_message(
                    message.chat.id,
                    "Select what would you like to edit",
                    reply_markup=edit_keyboard(),
                )
        except:
            bot.send_message(message.chat.id, "Please provide a valid ID")

    elif user.status == "changing deadline":
        i = 1
        id_edit = user.pop_task()
        for id_task, note, date in task.get_users_task():
            if i == int(id_edit):
                processed_date = process_date(text)
                task.update_deadline(task_id=id_task, new_date=processed_date)
                bot.send_message(
                    message.chat.id,
                    f"The deadline for task #{i} has been updated to {processed_date}.",
                    reply_markup = main_keyboard()
                )
            i += 1
        user.change_status("Start")

    elif user.status == "changing description":
        i = 1
        id_edit = user.pop_task()
        for id_task, note, date in task.get_users_task():
            if i == int(id_edit):
                bot.send_message(
                    message.chat.id,
                    f"The description for task #{i} has been updated to:\n{text}",
                    reply_markup = main_keyboard()
                )
                task.update_description(task_id=id_task, new_description=text)
            i += 1
        user.change_status("Start")

    else:
        bot.send_message(message.chat.id, "I do not even know what to say...")


@bot.callback_query_handler(func=lambda call: True)
def call_back_query(call):
    # adding a collab call_back
    if call.data == "cb_yes":
        bot.send_message(call.message.chat.id,"Provide a valid username of your friend in telegram\n(e.g. @prosto_kostik)")
        user = User(tel_id=call.from_user.id, user_name=call.from_user.username)
        user.change_status("adding collaborator")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Okay then")
    pass

def send_reminder():
    """Creates the query to database every 5 second"""
    print('it is running')
    info = extract_date()
    print(info)
    if type(info) == dict:
        print('info is')
        print(info["telegram_id"])
        task = Task(info["telegram_id"])
        bot.send_message(
            info["telegram_id"],
            f"Hey,a gentle reminder regarding your task:\n{info['task']}",
        )
        task.update_status(task_id=info["task_id"], new_status="inactive")
        if info['collaborator_id'] is not None:

            if type(info['collaborator_id']) == list:
                for name in info['collaborator_id']:
                    print(f"collab name{name}")
                    bot.send_message(
                    name,
                    f"Hey, your friend @{info['user_name']} created a task:\n{info['task']}",
                    )
            else:
                bot.send_message(
                info["collaborator_id"],
                f"Hey, your friend @{info['user_name']} created a task:\n{info['task']}",
                )
                pass
        task.update_status(task_id=info["task_id"], new_status="inactive")
    Timer(2, send_reminder).start()

Timer(2, send_reminder).start()

bot.infinity_polling()
