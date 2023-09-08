from telebot import types


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Add task'))
    markup.add(types.KeyboardButton('Remove task'))
    markup.add(types.KeyboardButton('Edit task'))
    markup.add(types.KeyboardButton('Show tasks'))
    return markup

def edit_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Change title'))
    markup.add(types.KeyboardButton('Change notes'))
    markup.add(types.KeyboardButton('Change date&time'))
    markup.add(types.KeyboardButton('Main menu'))
    return markup
    

