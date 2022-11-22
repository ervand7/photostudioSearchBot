from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message

from app import bot, dispatcher
from inline_keyboard.price import price_keyboard
from views.base import user_result

msg_from = 'Выберите цену от:'
msg_to = 'Выберите цену до:'


@dispatcher.message_handler(Text(equals=['Цена от'], ignore_case=True))
async def price_from(message: Message):
    await message.answer(msg_from, reply_markup=price_keyboard)


@dispatcher.message_handler(Text(equals=['Цена до'], ignore_case=True))
async def price_to(message: Message):
    await message.answer(msg_to, reply_markup=price_keyboard)


@dispatcher.callback_query_handler(text=[
    '500', '1000', '1500', '2000', '2500', '3000', '3500', '4000', '4500', '5000'
])
async def process_callback_price(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.message.text == msg_from:
        if user_result.price_to:
            if int(callback_query.data) > int(user_result.price_to):
                await bot.send_message(
                    callback_query.from_user.id,
                    text='<Цена от> не может быть выше <Цены до>',
                )
                return
        user_result.price_from = int(callback_query.data)
    else:
        if user_result.price_from:
            if int(callback_query.data) < int(user_result.price_from):
                await bot.send_message(
                    callback_query.from_user.id,
                    text='<Цена до> не может быть ниже <Цены от>',
                )
                return
        user_result.price_to = int(callback_query.data)

    await bot.send_message(
        callback_query.from_user.id,
        text=callback_query.data,
    )
