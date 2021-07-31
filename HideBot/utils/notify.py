from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from loguru import logger

from aiogram import Dispatcher
from asyncio import sleep

from data.payload import startup_text
from data.config import ADMINS_ID


async def on_startup_notify(dp: Dispatcher):
    logger.info("Admins notify...")
    for admin_id in ADMINS_ID:
        try:
            await dp.bot.send_message(admin_id, startup_text, disable_notification=True)
            logger.debug(f"Message send to - [{admin_id}]")
        except ChatNotFound:
            logger.warning("Chat with admin not found.")
        except BotBlocked:
            logger.warning("Admin blocked bot.")

        await sleep(0.2)
