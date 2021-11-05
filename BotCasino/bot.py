from aiogram import Dispatcher, executor
from loguru import logger

from loader import dp
from utils.notify import on_startup_notify
from utils.logger_config import setup_logger
from utils.middleware import setup_middlewares


async def on_startup(dispatcher: Dispatcher):
    setup_logger(level="DEBUG")
    setup_middlewares(dispatcher)
    logger.info("Setuping handlers...")
    import handlers

    await on_startup_notify(dispatcher)

    logger.info(f"Bot started succesfully!")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
