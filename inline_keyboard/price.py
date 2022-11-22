from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

price_keyboard = InlineKeyboardMarkup(row_width=2)
p500 = InlineKeyboardButton(text='500', callback_data='500')
p1000 = InlineKeyboardButton(text='1000', callback_data='1000')
p1500 = InlineKeyboardButton(text='1500', callback_data='1500')
p2000 = InlineKeyboardButton(text='2000', callback_data='2000')
p2500 = InlineKeyboardButton(text='2500', callback_data='2500')
p3000 = InlineKeyboardButton(text='3000', callback_data='3000')
p3500 = InlineKeyboardButton(text='3500', callback_data='3500')
p4000 = InlineKeyboardButton(text='4000', callback_data='4000')
p4500 = InlineKeyboardButton(text='4500', callback_data='4500')
p5000 = InlineKeyboardButton(text='5000', callback_data='5000')
price_keyboard.add(
    p500, p1000, p1500, p2000, p2500, p3000, p3500, p4000, p4500, p5000
)
