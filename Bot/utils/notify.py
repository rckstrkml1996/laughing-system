from asyncio import sleep

from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from aiogram import Dispatcher
from loguru import logger

from data.payload import startup_text
from config import config  # ADMINS_ID


async def on_startup_notify(dp: Dispatcher):
    logger.info("Admins notify...")
    try:
        for admin_id in config("admins_id"):
            try:
                await dp.bot.send_message(
                    admin_id, startup_text, disable_notification=True
                )
                logger.debug(f"Message send to - [{admin_id}]")
            except ChatNotFound:
                logger.warning("Chat with admin not found.")
            except BotBlocked:
                logger.warning("Admin blocked bot.")

            await sleep(0.2)
    except:
        pass
