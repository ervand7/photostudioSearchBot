from aiogram.types import ReplyKeyboardMarkup

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, )
menu_keyboard.row(
    'Дата',
    'Время с',
    'Время до',
    'Циклорама',
    'Цена от',
    'Цена до',
    'Окна',
    'Метраж от',
    'Метраж до',
    'Поиск',
)
