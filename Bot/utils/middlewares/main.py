from aiogram.types import Message
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger

from models import Worker
from loader import config
from data.texts import new_username_text, new_fullname_text
from utils import change_status


class KickMiddleware(BaseMiddleware):
    """Middleware to kick from workers"""

    def __init__(self, workers_chat=config.workers_chat):
        self.workers_chat = workers_chat
        super(KickMiddleware, self).__init__()  # in BaseMiddleware

    async def on_pre_process_message(self, message: Message, _):
        if message.chat.id == self.workers_chat:
            try:
                worker = Worker.get(cid=message.from_user.id)
                if worker.status < 2:  # not worker
                    await change_status.kick(self.workers_chat, message.from_user.id)
                    logger.info(
                        f"Kick user [{message.from_user.id}], user not autorized!"
                    )
            except Worker.DoesNotExist:
                logger.debug(
                    f"KickMiddleware - Worker [{message.from_user.id}] not found in base."
                )  # by bot logic user must be in base!
                await change_status.kick(self.workers_chat, message.from_user.id)
                logger.info(f"Kick user [{message.from_user.id}], user not autorized!")


class UpdateWorkerMiddleware(BaseMiddleware):
    """Middleware to update worker - username and fullname"""

    def __init__(self, workers_chat=config.workers_chat):
        self.workers_chat = workers_chat
        super(UpdateWorkerMiddleware, self).__init__()  # in BaseMiddleware

    async def on_pre_process_message(self, message: Message, _):
        try:
            worker = Worker.get(cid=message.from_user.id)
            if message.from_user.full_name != worker.name:
                if message.chat.id == self.workers_chat:
                    await message.reply(
                        new_fullname_text.format(
                            user_id=message.from_user.id,
                            old_name=worker.name,
                            new_name=message.from_user.full_name,
                        )
                    )
                worker.name = message.from_user.full_name
            if message.from_user.username != worker.username:
                if message.chat.id == self.workers_chat:
                    await message.reply(
                        new_username_text.format(
                            user_id=message.from_user.id,
                            name=message.from_user.full_name,
                            old_username=worker.username,
                            new_username=message.from_user.username,
                        )
                    )
                worker.username = message.from_user.username
            worker.save()
        except Worker.DoesNotExist:
            pass
