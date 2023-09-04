import telebot  
from telebot import types
from db import User

TOKEN = "6057584842:AAFLA0OfZhxQvcjTPpBgC7-IQTxp_iKWP1g"

bot = telebot.TeleBot(TOKEN)






@bot.message_handler(commands=['start'])
def start_record(message):

    global user
    user = User(message.from_user.id,message.from_user.username)
    user.insert_user()


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(types.KeyboardButton('Add task'))
    markup.add(types.KeyboardButton('Remove task'))
    markup.add(types.KeyboardButton('Edit task'))

    bot.send_message(
        message.chat.id,
        f"Hi {message.from_user.first_name},\nI was made to help your task managment!"
        ,reply_markup = markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Add task":
         bot.send_message(message.chat.id,"bip-bip")








@bot.message_handler(func = lambda m: True)
def results_save(message):
    bot.send_message(message, message.text)
    

@bot.message_handler(commands=['text'])
def record_task(message):
    user.insert_task(message.text,"10:08:2001")
    




bot.infinity_polling()