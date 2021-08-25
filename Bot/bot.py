import asyncio
import threading

from aiogram import Dispatcher
from uvicorn import Config, Server
from loguru import logger

from loader import dp, app, db_commands
from utils.pinner import dynapins
from utils.notify import on_startup_notify
from utils.logger_config import setup_logger
from utils.systeminfo import update_cpu_usage, exit_event
from utils.paysystem import check_payments
from utils.executional import setup_admins_statuses


async def on_startup(dispatcher: Dispatcher, notify=True):
    """
    Настройка всех компонентов для работы бота,
    Запуск бота
    """
    setup_logger(level="DEBUG")
    db_commands.setup_admins_statuses()
    logger.info("Setuping handlers...")
    import handlers

    if notify:
        await on_startup_notify(dispatcher)

    logger.info(f"Bot started succesfully...")


@app.on_event("shutdown")
async def api_shutdown():
    await shutdown_polling(dp)


async def shutdown(dispatcher: Dispatcher):
    dispatcher.stop_polling()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await dispatcher.bot.session.close()

    exit_event.set()

    for task in asyncio.all_tasks():
        task.cancel()

    # await dispatcher.wait_closed()


async def shutdown_polling(dispatcher: Dispatcher):
    # await on_shutdown()

    await shutdown(dispatcher)


async def start_bot(dispatcher: Dispatcher, notify=True):
    from utils import filters

    filters.setup(dispatcher)

    await dispatcher.skip_updates()
    await on_startup(dispatcher, notify=notify)
    await dispatcher.start_polling()


async def start_api(server):
    await server.serve()


def main():
    import api

    config = Config(
        app=app, loop=dp.bot.loop, lifespan="on", reload=True, host="0.0.0.0"
    )
    server = Server(config=config)

    loop = asyncio.get_event_loop()

    loop.create_task(dynapins(dp.bot))  # it runs in dispatcher)
    loop.create_task(check_payments())  # it runs in dispatcher)

    c_usage = threading.Thread(target=update_cpu_usage)
    c_usage.name = "CpuUsageUpdater"
    c_usage.start()

    started_bot = loop.create_task(start_bot(dp, notify=False))
    started_api = loop.create_task(start_api(server))

    try:
        loop.run_until_complete(asyncio.gather(started_api, started_bot))
    except asyncio.exceptions.CancelledError:
        logger.warning("Goodbye, sir!")
    except KeyboardInterrupt:
        loop.run_until_complete(shutdown_polling(dp))
    except Exception as e:
        print(e)
        loop.run_until_complete(shutdown_polling(dp))


if __name__ == "__main__":
    main()
