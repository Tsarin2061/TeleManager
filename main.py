import telebot  
from telebot import types
from db import User, Task


TOKEN = "6057584842:AAFLA0OfZhxQvcjTPpBgC7-IQTxp_iKWP1g"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_record(message):

    user = User(message.from_user.id,message.from_user.username,message.date)


    # if not user.check_db_for_user():
    #     user.insert_user()

    # creating buttons after start 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Add task'))
    markup.add(types.KeyboardButton('Remove task'))
    markup.add(types.KeyboardButton('Edit task'))
    markup.add(types.KeyboardButton('Show tasks'))

    # greating user
    bot.send_message(
        message.chat.id,
        f"Hi {message.from_user.first_name},\nI was made to help your task managment!"
        ,reply_markup = markup)


# buttons effects 
@bot.message_handler(content_types='text')
def handle_message(message):

    user = User(tel_id = message.from_user.id, 
                user_name = message.from_user.username, 
                log_time = message.date)
    
    if message.text == "Add task":
        bot.send_message(message.chat.id, "bip-bip for Add task")

    elif message.text == "Remove task":
        bot.send_message(message.chat.id, "bip-bip for Remove task")
    
    elif message.text == "Edit task":
        bot.send_message(message.chat.id, "bip-bip for Edit task")
    
    elif message.text == "Show tasks":
        bot.send_message(message.chat.id, "bip-bip for Show task")
    
    else:
        bot.send_message(message.chat.id, "I do not even know what to say...")









bot.infinity_polling()