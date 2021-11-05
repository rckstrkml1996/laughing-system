from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import BoundFilter

from models import Worker


class IsWorkerFilter(BoundFilter):
    key = "is_worker"  # working for query and message handlers

    def __init__(self, is_worker):
        self.is_worker = is_worker

    def get_target(self, obj):
        if isinstance(obj, CallbackQuery):
            return obj.from_user.id  # if query
        return obj.chat.id  # if message

    async def check(self, obj):
        user_id = self.get_target(obj)
        try:
            worker = Worker.get(cid=user_id)
            if self.is_worker == (worker.status >= 2):
                return {"worker": worker}
        except Worker.DoesNotExist:
            return not self.is_worker  # not worker


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
