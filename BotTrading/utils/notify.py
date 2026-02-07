from aiogram import Dispatcher
from aiogram.utils.exceptions import ChatNotFound, Unauthorized
from loguru import logger

from data.texts import startup_text
from loader import config


async def notify_admins(dispatcher: Dispatcher):
    for admin_id in config.admins_id:
        try:
            await dispatcher.bot.send_message(admin_id, startup_text)
        except ChatNotFound:
            logger.warning(f"ChatNotFound exception with - [{admin_id}]")
        except Unauthorized:
            logger.error(f"Unauthorized exception with - [{admin_id}]")
