from telebot import types


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Add task'))
    markup.add(types.KeyboardButton('Remove task'))
    markup.add(types.KeyboardButton('Edit task'))
    markup.add(types.KeyboardButton('Show tasks'))
    return markup

def sup_add_task_keyboard()

