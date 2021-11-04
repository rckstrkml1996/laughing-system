from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery

from models import EscortUser


class IsUser(BoundFilter):
    key = "is_user"
    required = True
    default = True

    def __init__(self, is_user):
        self.is_user = is_user

    def get_target(self, obj):
        if isinstance(obj, CallbackQuery):
            return obj.message.chat.id  # if query
        return obj.chat.id  # if message

    async def check(self, obj):
        chat_id = self.get_target(obj)

        try:
            user = EscortUser.get(cid=chat_id)
            if self.is_user == True:
                return {"user": user}
            return False
        except EscortUser.DoesNotExist:
            return self.is_user == False
