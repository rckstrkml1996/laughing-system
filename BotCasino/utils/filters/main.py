from aiogram.dispatcher.filters import BoundFilter
from loguru import logger

from models import CasinoUser




class IsWorking(BoundFilter):
    key = "is_working"  # working for query and message handlers
    required = True
    default = True

    def __init__(self, is_working):
        self.is_working = is_working

    def get_target(self, obj):
        return getattr(obj, "from_user", None)

    async def check(self, obj):
        user = self.get_target(obj)
        casino_work = config.casino_work

        try:
            user_work = not CasinoUser.get(cid=user.id).stopped
        except CasinoUser.DoesNotExist:
            user_work = True

        working = self.is_working == (casino_work and user_work)
        # logger.debug(f"IsWorking filter checked {working=}")
        return working
