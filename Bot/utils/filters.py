from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import BoundFilter

from models import Worker


class IsWorker(BoundFilter):
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
                pass
        return False


class SendSummary(BoundFilter):
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
