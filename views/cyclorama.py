from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message

from app import bot, dispatcher
from inline_keyboard.cyclorama import cyclorama_keyboard
from views.base import user_result

exists = 'Циклорама есть'
not_exists = 'Циклорамы нет'


@dispatcher.message_handler(Text(equals=['Циклорама'], ignore_case=True))
async def show_cyclorama(message: Message):
    await message.answer('Наличие циклорамы:', reply_markup=cyclorama_keyboard)


@dispatcher.callback_query_handler(text=[exists, not_exists])
async def process_callback_cyclorama(callback_query: CallbackQuery):
    user_result.cyclorama = True if callback_query.data == exists else False
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        text=callback_query.data,
    )
