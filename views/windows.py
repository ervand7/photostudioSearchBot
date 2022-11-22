from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message

from app import bot, dispatcher
from inline_keyboard.windows import windows_keyboard
from views.base import user_result

exists = 'Окна есть'
not_exists = 'Окон нет'


@dispatcher.message_handler(Text(equals=['Окна'], ignore_case=True))
async def show_windows(message: Message):
    await message.answer('Наличие окон:', reply_markup=windows_keyboard)


@dispatcher.callback_query_handler(text=[exists, not_exists])
async def process_callback_windows(callback_query: CallbackQuery):
    user_result.windows = True if callback_query.data == exists else False
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=callback_query.data,
    )
