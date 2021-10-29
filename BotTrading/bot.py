import sys
import asyncio

from aiogram import Dispatcher
from aiogram import executor


from loguru import logger
from loader import dp
from utils.notify import on_startup_notify
from utils.logger_config import setup_logger
from utils.fileidcreator import file_ids


async def on_startup(dispatcher: Dispatcher):
    setup_logger(level="INFO")
    logger.info("Установка обработчиков...")
    import handlers

    await on_startup_notify(dispatcher)

    logger.info(f"Бот успешно запущен...")


if __name__ == "__main__":
    if sys.platform == "win32":  # working even for win64!
        asyncio.set_event_loop(asyncio.SelectorEventLoop())

    from utils.filters import setup

    setup(dp)
    loop = asyncio.get_event_loop()
    loop.create_task(file_ids())
    executor.start_polling(
        dp, skip_updates=SKIP_UPDATES, on_startup=on_startup, timeout=4
    )
