import re

from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters import BoundFilter
from loguru import logger

from models import Worker


class IsWorkerFilter(BoundFilter):
    key = "is_worker"  # working for query and message handlers

    def __init__(self, is_worker):
        self.is_worker = is_worker

    def get_target(self, obj):
        if isinstance(obj, CallbackQuery):
            return obj.message.chat  # if query
        return obj.chat  # if message

    async def check(self, obj):
        chat = self.get_target(obj)
        if chat.type == "private":
            try:
                worker = Worker.get(cid=chat.id)
                if self.is_worker == (worker.status >= 2):
                    return {"worker": worker}
            except Worker.DoesNotExist:
                return not self.is_worker  # not worker
        else:
            return False

        # logger.debug(
        #     f"IsWorkerFilter called not in private chat and group, type: {chat.type}, id: {chat.id}"
        # )
        # return False


class IsAdminFilter(BoundFilter):
    key = "is_admin"  # working for query and message handlers

    def __init__(self, is_admin):
        self.is_admin = is_admin

    def get_target(self, obj):
        return getattr(obj, "from_user", None)

    async def check(self, obj):
        user = self.get_target(obj)
        try:
            worker = Worker.get(cid=user.id)
            if self.is_admin == (worker.status >= 5):
                return {"worker": worker}
        except Worker.DoesNotExist:
            return not self.is_admin  # not admin


class IsSupportFilter(BoundFilter):
    key = "is_support"  # working for query and message handlers

    def __init__(self, is_support):
        self.is_support = is_support

    def get_target(self, obj):
        return getattr(obj, "from_user", None)

    async def check(self, obj):
        user = self.get_target(obj)
        try:
            worker = Worker.get(cid=user.id)
            if self.is_support == (worker.status >= 3):
                return {"worker": worker}
        except Worker.DoesNotExist:
            return not self.is_support  # not admin
