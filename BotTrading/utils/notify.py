from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from loguru import logger

from aiogram import Dispatcher
from asyncio import sleep

from data.payload import startup_text



async def on_startup_notify(dp: Dispatcher):
    logger.info("Admins notify...")
    for admin_id in config.admins_id:
        try:
            await dp.bot.send_message(admin_id, startup_text, disable_notification=True)
            logger.debug(f"Message send to - [{admin_id}]")
        except ChatNotFound:
            logger.warning("Chat with admin not found.")
        except BotBlocked:
            logger.warning("Admin blocked bot.")
        except Exception as ex:
            logger.exception(ex)

        await sleep(0.2)
