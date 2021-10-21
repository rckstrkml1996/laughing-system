import asyncio
import threading
import sys

from aiogram import Dispatcher
from loguru import logger

from loader import dp, db_commands
from config import config, project_path, SKIP_UPDATES

from utils.pinner import dynapins
from utils.notify import on_startup_notify
from utils.logger_config import setup_logger
from utils.systeminfo import update_cpu_usage, exit_event
from utils.paysystem import check_qiwis
from utils.updaterepo import check_on_update
from utils.config_usernames import update_bot_usernames


async def on_startup(dispatcher: Dispatcher, notify=True, update_usernames=True):
    """
    Настройка всех компонентов для работы бота,
    Запуск бота
    """
    setup_logger(level="DEBUG")
    db_commands.setup_admins_statuses()
    logger.info("Setuping handlers...")
    import handlers

    if update_usernames:
        await update_bot_usernames()

    if notify:
        await on_startup_notify(dispatcher)


async def shutdown(dispatcher: Dispatcher):
    exit_event.set()
    dispatcher.stop_polling()

    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await dispatcher.bot.session.close()

    # await dispatcher.wait_closed()


async def shutdown_polling(dispatcher: Dispatcher):
    # await on_shutdown()

    await shutdown(dispatcher)


async def start_bot(dispatcher: Dispatcher, notify=True, skip_updates=True):
    from utils import filters, middlewares

    filters.setup(dispatcher)
    middlewares.setup(dispatcher)

    await on_startup(dispatcher, notify=notify)

    if skip_updates:
        await dispatcher.skip_updates()

    # logger.info(f"Bot started.")
    await dispatcher.start_polling(timeout=3)  # change if internet slow)


def main():
    # for aiohttp connection by proxy, too slow for windows :(
    if sys.platform == "win32":
        asyncio.set_event_loop(asyncio.SelectorEventLoop())

    loop = asyncio.get_event_loop()

    c_usage = threading.Thread(target=update_cpu_usage)
    c_usage.name = "CpuUsageUpdater"
    c_usage.start()

    # it runs in dispatcher)
    payments_f = loop.create_task(check_qiwis())
    dynamic_pins_f = loop.create_task(dynapins(dp.bot))

    # loop.create_task(AutoBtc())

    start_task = loop.create_task(
        start_bot(dp, notify=config("notify"), skip_updates=SKIP_UPDATES)
    )

    try:
        loop.run_until_complete(start_task)  # better for testing and dev
        # loop.run_forever() # better for static
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(shutdown_polling(dp))
        logger.warning("Poka!")


if __name__ == "__main__":
    check_on_update(project_path)
    main()
