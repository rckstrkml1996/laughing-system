import asyncio

from aiogram import Dispatcher
from aiogram import executor

from config import SKIP_UPDATES
from loguru import logger
from loader import dp

from utils.notify import on_startup_notify
from utils.logger_config import setup_logger
# from utils import life_outs


async def on_startup(dispatcher: Dispatcher):
    """
    Настройка всех компонентов для работы бота,
    Запуск бота
    """
    setup_logger(level="INFO")
    logger.info("Установка обработчиков...")
    import handlers

    await on_startup_notify(dispatcher)

    logger.info(f"Бот успешно запущен...")


# async def on_shutdown(dispatcher: Dispatcher):
#     for qiwi in qiwis:
#         await qiwis[qiwi].close()


if __name__ == '__main__':
    # dp.bot.loop.create_task(life_outs(dp.bot))
    executor.start_polling(dp, skip_updates=SKIP_UPDATES,
                           on_startup=on_startup)  # , on_shutdown=on_shutdown)
