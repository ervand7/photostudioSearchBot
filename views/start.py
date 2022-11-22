from aiogram.types import Message

from app import dispatcher
from inline_keyboard.main_menu import menu_keyboard


@dispatcher.message_handler(commands=['start'])
async def start(message: Message):
    await message.reply('Используйте ⌘', reply_markup=menu_keyboard)
