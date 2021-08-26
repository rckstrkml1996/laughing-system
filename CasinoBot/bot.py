import asyncio

from aiogram import Dispatcher
from aiogram import executor
from loguru import logger

from config import SKIP_UPDATES
from loader import dp

from utils.notify import on_startup_notify
from utils.logger_config import setup_logger


async def on_startup(dispatcher: Dispatcher):
    """
    Настройка всех компонентов для работы бота,
    Запуск бота
    """
    setup_logger(level="INFO")
    logger.info("Setuping handlers...")
    import handlers

    await on_startup_notify(dispatcher)

    logger.info(f"Bot started succesfully!")


if __name__ == "__main__":
    from utils import filters

    filters.setup(dp)
    executor.start_polling(
        dp, skip_updates=SKIP_UPDATES, on_startup=on_startup
    )  # , on_shutdown=on_shutdown)
