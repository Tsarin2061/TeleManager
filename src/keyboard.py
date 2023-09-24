from telebot import types


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Add task'))
    markup.add(types.KeyboardButton('Remove task'))
    markup.add(types.KeyboardButton('Edit task'))
    markup.add(types.KeyboardButton('Show tasks'))
    return markup

def collab_question_keyboard():
    pass

def remind_question_keyboard():
    pass

def edit_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Change description'))
    markup.add(types.KeyboardButton('Change deadline'))
    markup.add(types.KeyboardButton('Main menu'))
    return markup
    

