import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorHub

from Config.config import load_config, Config
from dialogs.start.SGDialogs import start_dialog
from handlers.user_handlers import user_router

from middlewares.i18n import TranslatorRunnerMiddleware
from middlewares.outer_middleware import PrivateMiddleware
from utils.i18n import create_translator_hub
from database.db_conf import database

format = '[{asctime}] #{levelname:8} {filename}:' \
         '{lineno} - {name} - {message}'

logging.basicConfig(
    level=logging.DEBUG,
    format=format,
    style='{'
)

logger = logging.getLogger(__name__)

#db = database('users_database')
#db.delete_data()

async def main():
    translator_hub: TranslatorHub = create_translator_hub()

    config: Config = load_config()

    bot = Bot(token=config.bot.token, parse_mode='HTML')
    dp = Dispatcher()

    # подключаем роутеры
    dp.include_routers(user_router, start_dialog)

    # подключаем middleware
    dp.update.outer_middleware(PrivateMiddleware())
    dp.update.middleware(TranslatorRunnerMiddleware())

    # запуск
    await bot.delete_webhook(drop_pending_updates=True)
    setup_dialogs(dp)
    logger.info('Bot start polling')
    await dp.start_polling(bot, _translator_hub=translator_hub)


if __name__ == "__main__":
    asyncio.run(main())