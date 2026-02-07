from aiogram import Dispatcher, executor

from loader import loop, dp, config, currency_worker
from utils.notify import notify_admins
from utils.logger_config import setup_logger
from utils.filters import setup_filters
from utils.middlewares import setup_middlewares
from handlers import register_handlers
from models import connect, disconnect


async def on_startup(dispatcher: Dispatcher):
    setup_logger(level="DEBUG")
    connect()
    setup_filters(dispatcher)
    setup_middlewares(dispatcher)
    loop.create_task(currency_worker.start_work())
    register_handlers(dispatcher)
    await notify_admins(dispatcher)


async def on_shutdown(_):
    currency_worker.stop_work()
    disconnect()


if __name__ == "__main__":
    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=config.skip_updates,
    )
