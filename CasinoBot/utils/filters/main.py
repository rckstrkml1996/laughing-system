from aiogram.dispatcher.filters import BoundFilter
from loguru import logger

from config import config  # ADMINS_ID


class IsWorking(BoundFilter):
    key = "is_working"  # working for query and message handlers
    required = True
    default = True

    def __init__(self, is_working):
        self.is_working = is_working

    async def check(self, obj):
        work = config("casino_work")
        logger.debug(f"IsWorking check work: {work}")
        return self.is_working == work
