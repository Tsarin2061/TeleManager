import telebot  
from db import User, Task
from keyboard import main_keyboard, edit_keyboard
from threading import Timer
from functions import extract_date

TOKEN = "6057584842:AAFLA0OfZhxQvcjTPpBgC7-IQTxp_iKWP1g"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_record(message):

    user = User(message.from_user.id,message.from_user.username)

    markup = main_keyboard()

    # greating user
    bot.send_message(
        message.chat.id,
        f"Hi {message.from_user.first_name},\nI was made to help your task managment!"
        ,reply_markup = markup)



# Define a dictionary to map commands to actions
commands = {
    "Add task": ("adding task", "Describe your task.",None),
    "Remove task": ("removing task", "Please provide the task ID for removal.",None),
    "Edit task": ("editing task", "To edit a task, please provide the task ID.", None),
    "Change deadline":("changing deadline", "Please provide the new task deadline (e.g., 10/08/2023 22:30)", None), 
    "Description": ("changing description", "bip-bip notes changing", None), 
    "Show tasks": ("showing tasks", "Your tasks bip-bip list:",None),
    "Main menu" : ("Start", "bip-bip for returning back", main_keyboard())
}

@bot.message_handler(content_types=['text'])
def handle_message(message):
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
            for id,note,date in task.get_users_task():
                bot.send_message(message.chat.id,f"№:{i}\nDescription: {note}\nDeadline: {date}")
                i+=1

    # Here we uses subprocesses
    elif user.status == 'adding task':
        user.change_status('adding task deadline')
        task.add_description(text)
        bot.send_message(message.chat.id, "Please provide the task deadline (e.g., 10/08/2023 22:30):")
    elif user.status == 'adding task deadline':
        task.add_deadline(text)
        bot.send_message(message.chat.id, "Done!\nBip-bip..")
        user.change_status('Start')
    elif user.status == 'removing task':
        to_remove = int(text)
        task.remove_users_task(to_remove)
        bot.send_message(message.chat.id, f"The task #{to_remove} has been successfully removed.\nBip-bip")
    elif user.status == 'editing task':
        global to_edit # sorry Kostik, I had no choice...
        to_edit = int(text)
        if to_edit:
            bot.send_message(message.chat.id, 'Select what would you like to edit',reply_markup = edit_keyboard())
    elif user.status == 'changing deadline':
        new_deadline = text
        task.update_deadline(task_id=to_edit,new_date=new_deadline)
        bot.send_message(message.chat.id,f"The deadline for task #{to_edit} has been updated to {new_deadline}.")
    elif user.status == 'changing description':
        new_task = text
        for id,note,date in task.get_users_task():
            if to_edit == id:
                bot.send_message(message.chat.id,f"Here's the current task description:\n{note}")
                task.update_description(task_id=to_edit,new_description=text)
    else:
        bot.send_message(message.chat.id, "I do not even know what to say...")

def send_reminder():
    info = extract_date()
    if info:
        task = Task(info['telegram_id'])
        bot.send_message(info['telegram_id'],f"Hey,a gentle reminder regarding your task:\n{info['task']}")
        task.update_status(task_id=info["task_id"], new_status='inactive')
    else:
        pass
    Timer(5,send_reminder).start()
Timer(5,send_reminder).start()

bot.infinity_polling()