from aiogram import Dispatcher, executor

from loguru import logger
from utils.notify import on_startup_notify
from utils.logger_config import setup_logger
from utils import filters, middlewares

from loader import dp, config


async def on_startup(dispatcher: Dispatcher):
    setup_logger(level="DEBUG")
    filters.setup(dispatcher)  # setup filters than create handlers
    middlewares.setup(dispatcher) # setup dont working middleware

    import handlers # setup it

    await on_startup_notify(dispatcher)
    logger.info("Bot started successfully!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=config.skip_updates, on_startup=on_startup)
