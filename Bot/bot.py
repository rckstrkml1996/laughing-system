import asyncio
import sys

from aiogram import Dispatcher
from aiogram import executor
from aiogram.utils.exceptions import NetworkError
from uvicorn import Config, Server
from loguru import logger

from loader import dp, app
from utils.notify import on_startup_notify
from utils.logger_config import setup_logger
from utils.filters import IsWorkerFilter, SendSummaryFilter, AdminsChatFilter, WorkersChatFilter


async def on_startup(dispatcher: Dispatcher, notify=True):
    """
    Настройка всех компонентов для работы бота,
    Запуск бота
    """
    setup_logger(level="DEBUG")
    logger.info("Setuping handlers...")
    import handlers

    if notify:
        await on_startup_notify(dispatcher)

    logger.info(f"Bot started succesfully...")


@app.on_event("shutdown")
async def api_shutdown():
    # print("SUSSUSSSAJAJSJ")
    await shutdown_polling(dp)


# async def on_shutdown():
#     pass


async def shutdown(dispatcher: Dispatcher):
    dispatcher.stop_polling()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    await dispatcher.bot.session.close()

    started_bot.cancel()
    # await dispatcher.wait_closed()  #


async def shutdown_polling(dispatcher: Dispatcher):
    # await on_shutdown()

    await shutdown(dispatcher)


async def start_bot(dispatcher: Dispatcher, notify=True):
    dispatcher.filters_factory.bind(IsWorkerFilter)
    dispatcher.filters_factory.bind(SendSummaryFilter)
    dispatcher.filters_factory.bind(AdminsChatFilter)
    dispatcher.filters_factory.bind(WorkersChatFilter)

    await dispatcher.skip_updates()
    await on_startup(dispatcher, notify=notify)
    await dispatcher.start_polling()


async def start_api(server):
    await server.serve()


def main():
    # import api
    config = Config(app=app, loop=dp.bot.loop, lifespan="on",
                    reload=True, host="0.0.0.0")
    server = Server(config=config)
    loop = asyncio.get_event_loop()

    global started_bot
    started_bot = loop.create_task(start_bot(dp, notify=True))
    started_api = loop.create_task(start_api(server))

    # loop.run_until_complete(started_bot)
    try:
        loop.run_until_complete(asyncio.gather(started_api, started_bot))
    except KeyboardInterrupt:
        print("GG Boy!")  # not used!


if __name__ == "__main__":
    main()
