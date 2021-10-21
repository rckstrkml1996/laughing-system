from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from loguru import logger

from aiogram import Dispatcher
from asyncio import sleep

from config import config
from data.payload import startup_text


async def on_startup_notify(dp: Dispatcher, sleep_time = 0.2):
    logger.info("Notifying admins...")
    for admin_id in config("admins_id"):
        try:
            await dp.bot.send_message(admin_id, startup_text, disable_notification=True)
            logger.debug(f"Send notify message to [{admin_id}]")
        except ChatNotFound:
            logger.warning(f"Admin not notified, ChatNotFound with [{admin_id}]")
        except BotBlocked:
            logger.warning(f"Admin not notified, BotBlocked with [{admin_id}]")

        await sleep(sleep_time)
