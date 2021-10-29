from asyncio import sleep

from aiogram.utils.exceptions import ChatNotFound, BotBlocked, CantInitiateConversation
from aiogram import Dispatcher
from loguru import logger

from data.payload import startup_text, updated_startup_text



async def on_startup_notify(dp: Dispatcher):
    if config.updated:
        config.updated = False
        text = updated_startup_text
    else:
        text = startup_text

    logger.info("Admins notify...")
    for admin_id in config.admins_id:
        try:
            await dp.bot.send_message(admin_id, text, disable_notification=True)
            logger.debug(f"Notify message send to admin: [{admin_id}]")
        except ChatNotFound:
            logger.warning("Chat with admin not found.")
        except BotBlocked:
            logger.warning("Admin blocked bot.")
        except CantInitiateConversation:
            logger.warning(f"Cant initiate conversation with user: [{admin_id}]")
        except:
            logger.error(f"Admins notify exception")

        await sleep(0.2)

    try:
        admins_chat = config.admins_chat
        await dp.bot.send_message(admins_chat, text, disable_notification=True)
        logger.debug(f"Notify message send to Admins Chat {admins_chat}")
        await sleep(0.2)
        workers_chat = config.workers_chat
        await dp.bot.send_message(workers_chat, text, disable_notification=True)
        logger.debug(f"Notify message send to Admins Chat {admins_chat}")
    except:
        logger.warning("Chats notify exception")
