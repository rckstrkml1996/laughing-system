from aiogram.dispatcher.filters import BoundFilter

from models import TradingUser


class IsUser(BoundFilter):
    key = "is_user"
    required = False
    default = False

    def __init__(self, is_user):
        self.is_user = is_user

    async def check(self, obj):
        user_id = obj.from_user.id

        try:
            user = TradingUser.get(cid=user_id)
            if self.is_user == True:
                return {"user": user}
            else:
                return False
        except TradingUser.DoesNotExist:
            return self.is_user == False
