from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

search_keyboard = InlineKeyboardMarkup(row_width=1)
button = InlineKeyboardButton(text='Поиск', callback_data='Поиск')
search_keyboard.add(button)
