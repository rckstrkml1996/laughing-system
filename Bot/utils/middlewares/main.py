from aiogram.types import Message
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger

from models import Worker
from loader import config
from data.texts import new_username_text


# from time import time  # for check speed
class NewUsernameMiddleware(BaseMiddleware):
    def __init__(self, chat=config.workers_chat):
        self.chat = chat
        super(NewUsernameMiddleware, self).__init__()  # resrive in BaseMiddleware

    async def on_process_message(self, message: Message, data: dict):
        try:
            worker = Worker.get(cid=message.from_user.id)
            if worker.username != message.from_user.username:
                if message.chat.id == self.chat:
                    await message.reply(
                        new_username_text.format(
                            chat_id=worker.cid,
                            name=worker.name,
                            old_username=worker.username,
                            new_username=message.from_user.username,
                        )
                    )
                worker.username = message.from_user.username
                worker.save()  # save new username in base

            if worker.name != message.from_user.full_name:
                worker.name = message.from_user.full_name
                worker.save()  # save new fullname in base
        except Worker.DoesNotExist:
            logger.debug(
                f"NewUsernameMiddleware - Worker [{message.from_user.id}] not found in base."
            )
