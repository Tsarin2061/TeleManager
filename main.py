import telebot  
from telebot import types
from db import User, Task
from keyboard import main_keyboard, edit_keyboard


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
    "Add task": ("adding task", "Describe your task!",None),
    "Remove task": ("removing task", "bip-bip for Remove task",None),
    "Edit task": ("editing task", "bip-bip for Edit task", edit_keyboard()),
    "Change title": ("changing title", "bip-bip titlechanging", None),  # Special case
    "Change date&time":("changing date", "bip-bip date changing", None), # under editing task
    "Change notes": ("changing notes", "bip-bip notes changing", None),  # Special case
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
            for id,note,date in task.get_users_task():
                bot.send_message(message.chat.id,f"№:{id}\nDescription: {note}\nDeadline: {date}")
                

    # Here we add task
    elif user.status == 'adding task':
        user.change_status('adding task deadline')
        task.add_description(text)
        bot.send_message(message.chat.id, "Please provide the task deadline (e.g., 10/08/2023 22:30):")
    elif user.status == 'adding task deadline':
        task.add_deadline(text)
        bot.send_message(message.chat.id, "Done!\nBip-bip..")
        user.change_status('Start')
    else:
        bot.send_message(message.chat.id, "I do not even know what to say...")




bot.infinity_polling()