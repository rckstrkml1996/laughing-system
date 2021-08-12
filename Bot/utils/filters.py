from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import BoundFilter

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
        return False


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
    key = 'admins_type'
    required = True
    default = False

    def get_target(self, obj):
        if isinstance(obj, CallbackQuery):
            return obj.message.chat  # if query
        return obj.chat  # if message

    def __init__(self, admins_type):
        self.admins_type = admins_type

    async def check(self, obj):
        chat = self.get_target(obj)
        if chat.id == config("admins_chat"):
            return self.admins_type
        return not self.admins_type


class WorkersChatFilter(BoundFilter):
    key = 'workers_type'
    required = True
    default = False

    def get_target(self, obj):
        if isinstance(obj, CallbackQuery):
            return obj.message.chat  # if query
        return obj.chat  # if message

    def __init__(self, workers_type):
        self.workers_type = workers_type

    async def check(self, obj):
        chat = self.get_target(obj)
        if chat.id == config("workers_chat"):
            return self.workers_type
        return not self.workers_type
