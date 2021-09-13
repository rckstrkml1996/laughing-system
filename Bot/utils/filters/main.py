from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import BoundFilter
from loguru import logger

from config import config  # ADMINS_ID
from customutils.models import Worker


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
                return self.is_worker == (Worker.get(cid=chat.id).status >= 2)
            except Worker.DoesNotExist:
                return not self.is_worker  # not worker
        elif chat.type == "group" or "supergroup":
            return False

        logger.debug(
            f"IsWorkerFilter called not in private chat and group, type: {chat.type}, id: {chat.id}"
        )
        return False


class IsAdminFilter(BoundFilter):
    key = "is_admin"  # working for query and message handlers

    def __init__(self, is_admin):
        self.is_admin = is_admin

    def get_target(self, obj):
        return getattr(obj, "from_user", None)

    async def check(self, obj):
        user = self.get_target(obj)
        try:
            return self.is_admin == (Worker.get(cid=user.id).status >= 5)
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
            return self.is_support == (Worker.get(cid=user.id).status >= 3)
        except Worker.DoesNotExist:
            return not self.is_support  # not admin


class SendSummaryFilter(BoundFilter):
    key = "send_summary"  # working for query and message handlers

    def __init__(self, send_summary):
        self.send_summary = send_summary

    def get_target(self, obj):
        if isinstance(obj, CallbackQuery):
            return obj.message.chat  # if query
        return obj.chat  # if message

    async def check(self, obj):
        chat = self.get_target(obj)
        if chat.type == "private":
            try:
                return Worker.get(cid=chat.id).send_summary == self.send_summary
            except Worker.DoesNotExist:
                pass
        return False


class AdminsChatFilter(BoundFilter):
    key = "admins_chat"
    required = True
    default = False

    def get_target(self, obj):
        if isinstance(obj, CallbackQuery):
            return obj.message.chat  # if query
        return obj.chat  # if message

    def __init__(self, admins_chat):
        self.admins_chat = admins_chat

    async def check(self, obj):
        chat = self.get_target(obj)
        if chat.id == config("admins_chat"):
            return self.admins_chat
        return not self.admins_chat


class WorkersChatFilter(BoundFilter):
    key = "workers_chat"
    required = True
    default = False

    def get_target(self, obj):
        if isinstance(obj, CallbackQuery):
            return obj.message.chat  # if query
        return obj.chat  # if message

    def __init__(self, workers_chat):
        self.workers_chat = workers_chat

    async def check(self, obj):
        chat = self.get_target(obj)
        if chat.id == config("workers_chat"):
            return self.workers_chat
        return not self.workers_chat
