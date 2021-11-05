from asyncio import sleep

from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from aiogram import Dispatcher
from loguru import logger

from loader import config
from data.texts import startup


async def on_startup_notify(dp: Dispatcher):
    logger.info("Notify admins...")
    for admin_id in config.admins_id:
        try:
            await dp.bot.send_message(admin_id, startup, disable_notification=True)
            logger.debug(f"Message send [{admin_id}]")
        except ChatNotFound:
            logger.warning(f"Chat with admin [{admin_id}] not found")
        except BotBlocked:
            logger.warning(f"Admin [{admin_id}] blocked bot")

        await sleep(0.1)
