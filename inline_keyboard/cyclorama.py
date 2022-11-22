from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cyclorama_keyboard = InlineKeyboardMarkup(row_width=1)
yes = InlineKeyboardButton(text='Циклорама есть', callback_data='Циклорама есть')
no = InlineKeyboardButton(text='Циклорамы нет', callback_data='Циклорамы нет')
cyclorama_keyboard.add(yes, no)
