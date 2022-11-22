import datetime
from typing import Dict

from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message
from inline_timepicker.inline_timepicker import InlineTimepicker

from app import dispatcher, bot
from views.base import user_result

inline_timepicker = InlineTimepicker()
start_text = 'Дата начала:'
end_text = 'Дата конца:'


@dispatcher.message_handler(Text(equals=['Время с'], ignore_case=True))
async def start_time(message: Message):
    inline_timepicker.init(
        datetime.time(12),
        datetime.time(1),
        datetime.time(23),
    )
    await bot.send_message(
        message.from_user.id,
        text=start_text,
        reply_markup=inline_timepicker.get_keyboard()
    )


@dispatcher.message_handler(Text(equals=['Время до'], ignore_case=True))
async def stop_time(message: Message):
    inline_timepicker.init(
        datetime.time(12),
        datetime.time(1),
        datetime.time(23),
    )
    await bot.send_message(
        message.from_user.id,
        text=end_text,
        reply_markup=inline_timepicker.get_keyboard()
    )


@dispatcher.callback_query_handler(inline_timepicker.filter())
async def time_handler(query: CallbackQuery, callback_data: Dict[str, str]):
    await query.answer()
    handle_result = inline_timepicker.handle(query.from_user.id, callback_data)

    if handle_result is not None:
        if query.message.text == start_text:
            user_result.time_start = handle_result
        elif query.message.text == end_text:
            user_result.time_end = handle_result
        await bot.edit_message_text(
            handle_result,
            chat_id=query.from_user.id,
            message_id=query.message.message_id
        )
    else:
        await bot.edit_message_reply_markup(
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            reply_markup=inline_timepicker.get_keyboard()
        )
