import threading

from aiogram import Dispatcher, executor
from loguru import logger

from loader import config, dp
from utils.pinner import dynapins
from utils.notify import on_startup_notify
from utils.logger_config import setup_logger
from utils.systeminfo import update_cpu_usage, exit_event
from utils.paysystem import check_qiwis
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

    dispatcher.loop.create_task(check_qiwis()) # or may be from loader import loop??
    dispatcher.loop.create_task(dynapins(dp.bot))


async def on_shutdown(dispatcher: Dispatcher):
    exit_event.set()


# async def start_bot(dispatcher: Dispatcher, notify=True, skip_updates=True):
#     


#     await on_startup(dispatcher, notify=notify)

#     if skip_updates:
#         await dispatcher.skip_updates()

#     # logger.info(f"Bot started.")
#     await dispatcher.start_polling(timeout=3)  # change if internet slow)


def main():
    c_usage = threading.Thread(target=update_cpu_usage)
    c_usage.name = "CpuUsageUpdater"
    c_usage.start()

    executor.start_polling(
        dp, skip_updates=config.skip_updates, on_startup=on_startup, on_shutdown=on_shutdown
    )

    # tasks = asyncio.gather(
    #     loop.create_task(check_qiwis()),
    #     loop.create_task(dynapins(dp.bot)),
    #     loop.create_task(
    #         start_bot(dp, notify=config.notify, skip_updates=config.skip_updates)
    #     )
    # )

    # try:
    #     loop.run_until_complete(tasks)  # better for testing and dev
    # except (KeyboardInterrupt, SystemExit):
    #     pass
    # finally:
    #     loop.run_until_complete(shutdown_polling(dp))
    #     logger.warning("Poka!")


if __name__ == "__main__":
    main()
