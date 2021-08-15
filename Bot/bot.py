import asyncio

from aiogram import Dispatcher
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
    setup_logger(level="INFO")
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

    for task in asyncio.all_tasks():
        task.cancel()

    # await dispatcher.wait_closed()  #


async def shutdown_polling(dispatcher: Dispatcher):
    # await on_shutdown()

    await shutdown(dispatcher)


async def start_bot(dispatcher: Dispatcher, notify=True):
    event_handlers = [
        dispatcher.message_handlers,
        dispatcher.edited_message_handlers,
        dispatcher.callback_query_handlers,
    ]

    dispatcher.filters_factory.bind(
        IsWorkerFilter, event_handlers=event_handlers)
    dispatcher.filters_factory.bind(
        SendSummaryFilter, event_handlers=event_handlers)
    dispatcher.filters_factory.bind(
        AdminsChatFilter, event_handlers=event_handlers)
    dispatcher.filters_factory.bind(
        WorkersChatFilter, event_handlers=event_handlers)

    await dispatcher.skip_updates()
    await on_startup(dispatcher, notify=notify)
    await dispatcher.start_polling()


async def start_api(server):
    await server.serve()


def main():
    import api
    config = Config(app=app, loop=dp.bot.loop, lifespan="on",
                    reload=True, host="0.0.0.0")
    server = Server(config=config)
    loop = asyncio.get_event_loop()

    # loop.create_task(dynapins(bot))  # it runs in dispatcher)

    started_bot = loop.create_task(start_bot(dp, notify=True))
    started_api = loop.create_task(start_api(server))

    try:
        loop.run_until_complete(
            asyncio.gather(
                started_api, started_bot
            )
        )
    except asyncio.exceptions.CancelledError:
        pass
    except KeyboardInterrupt:
        print("GG Boy!")  # not used!


if __name__ == "__main__":
    main()
