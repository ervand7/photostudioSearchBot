from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message

from app import bot, dispatcher
from inline_keyboard.footage import footage_keyboard
from views.base import user_result

msg_from = 'Выберите метраж от (квадратные метры):'
msg_to = 'Выберите метраж до (квадратные метры):'


@dispatcher.message_handler(Text(equals=['Метраж от'], ignore_case=True))
async def footage_from(message: Message):
    await message.answer(msg_from, reply_markup=footage_keyboard)


@dispatcher.message_handler(Text(equals=['Метраж до'], ignore_case=True))
async def footage_to(message: Message):
    await message.answer(msg_to, reply_markup=footage_keyboard)


@dispatcher.callback_query_handler(text=[
    '30', '40', '50', '60', '70', '80',
    '90', '100', '110', '120', '130', '140', '150'
])
async def process_callback_footage(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.message.text == msg_from:
        if user_result.footage_to:
            if int(callback_query.data) > int(user_result.footage_to):
                await bot.send_message(
                    callback_query.from_user.id,
                    text='<Метраж от> не может быть выше <Метража до>',
                )
                return
        user_result.footage_from = int(callback_query.data)
    else:
        if user_result.footage_from:
            if int(callback_query.data) < int(user_result.footage_from):
                await bot.send_message(
                    callback_query.from_user.id,
                    text='<Метраж до> не может быть ниже <Метража от>',
                )
                return
        user_result.footage_to = int(callback_query.data)
    await bot.send_message(
        callback_query.from_user.id,
        text=callback_query.data,
    )
