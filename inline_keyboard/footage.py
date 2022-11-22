from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

footage_keyboard = InlineKeyboardMarkup(row_width=2)
f30 = InlineKeyboardButton(text='30', callback_data='30')
f40 = InlineKeyboardButton(text='40', callback_data='40')
f50 = InlineKeyboardButton(text='50', callback_data='50')
f60 = InlineKeyboardButton(text='60', callback_data='60')
f70 = InlineKeyboardButton(text='70', callback_data='70')
f80 = InlineKeyboardButton(text='80', callback_data='80')
f90 = InlineKeyboardButton(text='90', callback_data='90')
f100 = InlineKeyboardButton(text='100', callback_data='100')
f110 = InlineKeyboardButton(text='110', callback_data='110')
f120 = InlineKeyboardButton(text='120', callback_data='120')
f130 = InlineKeyboardButton(text='130', callback_data='130')
f140 = InlineKeyboardButton(text='140', callback_data='140')
f150 = InlineKeyboardButton(text='150', callback_data='150')
footage_keyboard.add(
    f30, f40, f50, f60, f70, f80, f90, f100, f110, f120, f130, f140, f150,
)
