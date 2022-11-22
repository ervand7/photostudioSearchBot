import logging
import os

from aiogram import Bot, Dispatcher
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_API_TOKEN)
dispatcher = Dispatcher(bot)

_options = Options()
_options.add_argument("headless")
_options.add_argument("--no-sandbox")
driver = webdriver.Remote(
    command_executor=os.getenv('SELENIUM_DRIVER_HOST'),
    options=_options
)
