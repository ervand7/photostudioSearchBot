from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message
from aiogram.utils.callback_data import CallbackData
from aiogram_calendar import SimpleCalendar, simple_cal_callback

from app import dispatcher
from inline_keyboard.main_menu import menu_keyboard
from views.base import user_result


@dispatcher.message_handler(Text(equals=['Дата'], ignore_case=True))
async def calendar(message: Message):
    await message.answer(
        "Дата:", reply_markup=await SimpleCalendar().start_calendar()
    )


@dispatcher.callback_query_handler(simple_cal_callback.filter())
async def process_calendar(
        callback_query: CallbackQuery, callback_data: CallbackData
):
    selected, date = \
        await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        user_result.date = date
        await callback_query.message.answer(
            user_result.date.date(),
            reply_markup=menu_keyboard
        )
