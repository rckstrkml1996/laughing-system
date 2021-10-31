from asyncio import sleep

from loguru import logger

from models import Worker, Profit
from utils.render import render_profit
from utils import basefunctional


class PayChecker:
    SERVICE_NAMES = ["Казино", "Эскорт", "Трейдинг", "Прямой перевод"]

    def __init__(self, sleep_time: int = 50):
        self._working = False
        self.sleep_time = sleep_time

    def work(self):
        self._working = True
        logger.debug("PayChecker working.")

    def stop(self):
        self._working = False

    async def check_casino(self):
        pass

    async def start(self):
        self.work()

        profit = Profit.create(
            owner=Worker.get(),
            amount=123,
            share=100,
        )

        while self._working:
            await self.send_profit(profit)

            await sleep(self.sleep_time, int)

    async def send_profit(self, profit: Profit):
        all_profit = basefunctional.get_profits_sum(profit.owner.id)
        rendered_profit_path = render_profit(
            all_profit,
            profit.amount,
            profit.share,
            self.SERVICE_NAMES[profit.service],
            profit.owner.username,
            "...",  # analog text
        )
        print(rendered_profit_path)
