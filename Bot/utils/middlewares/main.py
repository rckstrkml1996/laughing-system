from aiogram.types import Message
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger

from models import Worker
from loader import config
from data.texts import new_username_text
from utils import change_status


class AllMiddleware(BaseMiddleware):
    """Middleware to kick and change username for workers"""

    def __init__(self, chat=config.workers_chat):
        self.chat = chat
        super(AllMiddleware, self).__init__()  # in BaseMiddleware

    async def make(self, message: Message, _: dict):
        try:
            worker = Worker.get(cid=message.from_user.id)
            if message.chat.id == self.chat and worker.status < 2:  # not worker
                await change_status.kick(self.chat, message.from_user.id)
                logger.info(f"Kick user [{message.from_user.id}], user not autorized!")

            if worker.name != message.from_user.full_name:
                worker.name = message.from_user.full_name
                worker.save()  # save new fullname in base

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
        except Worker.DoesNotExist:
            logger.debug(
                f"NewUsernameMiddleware - Worker [{message.from_user.id}] not found in base."
            )  # by bot logic user must be in base!
            if message.chat.id == self.chat:
                await change_status.kick(self.chat, message.from_user.id)
                logger.info(f"Kick user [{message.from_user.id}], user not autorized!")
