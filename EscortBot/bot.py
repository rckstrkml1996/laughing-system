import sys
import asyncio

from aiogram import Dispatcher, executor
from loguru import logger

from loader import dp
from utils.notify import on_startup_notify
from utils.logger_config import setup_logger


async def on_startup(dispatcher: Dispatcher):
    """
    Настройка всех компонентов для работы бота,
    Запуск бота
    """
    from utils import filters

    filters.setup(dispatcher)

    setup_logger(level="INFO")
    logger.info("Установка обработчиков...")
    import handlers

    await on_startup_notify(dispatcher)

    logger.info(f"Бот успешно запущен...")


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop(asyncio.SelectorEventLoop())

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, timeout=4)
