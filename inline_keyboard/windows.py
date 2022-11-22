from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

windows_keyboard = InlineKeyboardMarkup(row_width=1)
yes = InlineKeyboardButton(text='Окна есть', callback_data='Окна есть')
no = InlineKeyboardButton(text='Окон нет', callback_data='Окон нет')
windows_keyboard.add(yes, no)
