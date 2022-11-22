from aiogram.types import Message

from app import dp
from inline_keyboard.main_menu import menu


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.reply('Используйте ⌘', reply_markup=menu)
