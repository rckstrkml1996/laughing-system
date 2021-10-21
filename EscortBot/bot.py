from aiogram import Dispatcher, executor

from loguru import logger
from utils.notify import on_startup_notify
from utils.logger_config import setup_logger
from utils.filters import setup
from config import config
from loader import dp


async def on_startup(dispatcher: Dispatcher):
    setup_logger(level="DEBUG")
    setup(dp)  # setup filters than create handlers

    import handlers

    await on_startup_notify(dp)
    logger.info("Bot started successfully!")


if __name__ == "__main__":
    executor.start_polling(
        dp, skip_updates=config("skip_updates", bool), on_startup=on_startup
    )
