from time import sleep

from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message

from app import bot, dispatcher
from controllers.photoplace_pro import photoplacepro_fabric
from controllers.studiorent import studiorent_fabric
from controllers.ugoloc import ugoloc_fabric
from inline_keyboard.search import search_keyboard
from views.base import user_result

SEARCH_TIMEOUT = 1


class Answer:
    def __init__(self, callback_query: CallbackQuery):
        self.callback_query = callback_query

    def send_message(self, message: str):
        return bot.send_message(
            self.callback_query.from_user.id,
            text=message,
        )

    def wrong_time(self):
        return bot.send_message(
            self.callback_query.from_user.id,
            text='Время начала не может быть больше времени конца',
        )

    def not_found(self):
        return bot.send_message(
            self.callback_query.from_user.id,
            text='По заданным параметрам студии не нашлись ☹️',
        )

    def progress_bar(self, message: str):
        return bot.send_message(
            self.callback_query.from_user.id,
            text=message,
        )


@dispatcher.message_handler(Text(equals=['Поиск'], ignore_case=True))
async def show_search(message: Message):
    await message.answer('Начнем поиск?', reply_markup=search_keyboard)


@dispatcher.callback_query_handler(text='Поиск')
async def process_callback_search(callback_query: CallbackQuery):
    answer = Answer(callback_query)
    await bot.answer_callback_query(callback_query.id)
    if user_result.time_start and user_result.time_end:
        if user_result.time_start > user_result.time_end:
            await answer.wrong_time()
            return

    data = {
        studiorent_fabric: 'https://www.studiorent.ru',
        ugoloc_fabric: 'https://ugoloc.ru/',
        photoplacepro_fabric: 'https://photoplace.pro/moscow'
    }
    for index, (func, site_name) in enumerate(data.items()):
        await answer.progress_bar(
            f"""😍 {"Ищем" if index == 0 else "Теперь ищем "} на сайте: {
            site_name} 😍\n\nПоиск может занять до нескольких минут...""")
        studios = _studios = await func(user_result)

        if len(studios) == 0:
            await answer.not_found()
            continue
        batch_size = 20
        while studios:
            message = ''
            studios_batch = studios[:batch_size]
            for name, link in studios_batch:
                message += f'{name} {link}\n'
            await answer.send_message(message)
            studios = studios[batch_size:]
        await answer.send_message(f'Найденное кол-во на этом сайте: {len(_studios)}')
        sleep(SEARCH_TIMEOUT)
    user_result.reset()
