import threading

from aiogram import Dispatcher, executor
from loguru import logger

from loader import config, dp, dynapinner, payments_checker
from utils.notify import on_startup_notify
from utils.logger_config import setup_logger
from utils.systeminfo import update_cpu_usage, exit_event
from utils.updaterepo import check_on_update
from utils.config_usernames import update_bot_usernames


async def on_startup(dispatcher: Dispatcher):
    setup_logger(level="DEBUG")

    from utils import filters, middlewares

    filters.setup(dispatcher)
    middlewares.setup(dispatcher)

    logger.info("Setuping handlers...")
    import handlers

    await update_bot_usernames()

    check_on_update()
    if config.notify:
        await on_startup_notify(dispatcher)

    dispatcher.loop.create_task(
        payments_checker.start()
    )  # or may be from loader import loop??
    # dispatcher.loop.create_task(dynapinner.start())


async def on_shutdown(_: Dispatcher):
    exit_event.set()

    payments_checker.stop()
    dynapinner.stop()


def main():
    c_usage = threading.Thread(target=update_cpu_usage)
    c_usage.name = "CpuUsageUpdater"
    c_usage.start()

    executor.start_polling(
        dp,
        skip_updates=config.skip_updates,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        timeout=5,
    )


if __name__ == "__main__":
    main()
