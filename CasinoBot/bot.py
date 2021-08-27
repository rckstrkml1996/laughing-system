import asyncio
import sys

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


async def shutdown(dispatcher: Dispatcher):
    dispatcher.stop_polling()

    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await dispatcher.bot.session.close()

    # await dispatcher.wait_closed()


async def start_bot(dispatcher: Dispatcher):
    from utils import filters

    filters.setup(dispatcher)

    await on_startup(dispatcher)

    await dispatcher.skip_updates()
    logger.info(f"Starting bot...")
    await dispatcher.start_polling(timeout=5)  # change if internet slow)


if __name__ == "__main__":
    if sys.platform == "win32":  # working even for win64!
        asyncio.set_event_loop(asyncio.SelectorEventLoop())

    loop = asyncio.get_event_loop()
    started_task = loop.create_task(start_bot(dp))

    try:
        loop.run_until_complete(started_task)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(shutdown(dp))

    # executor.start_polling(
    #     dp, skip_updates=SKIP_UPDATES, on_startup=on_startup
    # )  # , on_shutdown=on_shutdown)
