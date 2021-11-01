from asyncio import sleep
from typing import Union

from aiogram import Bot
from aiogram.types import InputFile
from loguru import logger

from customutils import BotConfig
from models import (
    Worker,
    Profit,
    QiwiPayment,
    CasinoPayment,
    EscortPayment,
    TradingPayment,
)
from data.texts import chat_profit_text, outs_profit_text, admins_profit_text
from utils.render import render_profit
from utils import basefunctional


class PayChecker:
    SERVICE_NAMES = ["Казино", "Эскорт", "Трейдинг", "Прямой перевод"]

    def __init__(self, bot: Bot, config: BotConfig):
        if not isinstance(bot, Bot):
            raise TypeError(
                f"Argument 'bot' must be an instance of Bot, not '{type(bot).__name__}'"
            )

        self.bot = bot
        self.config = config

        self._working = False

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

            await sleep(self.config.qiwi_check_time, int)

    async def send_profit(
        self,
        profit: Profit,
        payment: Union[CasinoPayment, EscortPayment, TradingPayment] = None,
    ):
        worker: Worker = profit.owner
        qiwi_payment: QiwiPayment = profit.payment

        all_profit = basefunctional.get_profits_sum(worker.id)
        rendered_profit_path = render_profit(
            all_profit,
            profit.amount,
            profit.share,
            self.SERVICE_NAMES[profit.service],  # refactor
            worker.username,
            "...",  # analog text
        )

        mention = (  # get mention
            "Скрылся"
            if worker.username_hide
            else (
                f"@{worker.username}"
                if worker.username is not None
                else f"<a ref='tg://user?id={worker.cid}'>{worker.name}</a>"
            )
        )
        outs_msg = await self.bot.send_photo(
            self.config.outs_chat,
            InputFile(rendered_profit_path),
            caption=outs_profit_text.format(
                service=self.SERVICE_NAMES[profit.service],  # refactor
                amount=profit.amount,
                share=profit.share,
                mention=mention,
            ),
        )
        if self.config.profit_sticker_id is not None:
            await self.bot.send_sticker(  # try: except:
                self.config.workers_chat, self.config.profit_sticker_id
            )
        await self.bot.send_message(  # send info about profit in workers chat
            self.config.workers_chat,
            chat_profit_text.format(
                profit_link=outs_msg.url,
                service=self.SERVICE_NAMES[profit.service],  # refactor
                amount=profit.amount,
                share=profit.share,
                mention=mention,
            ),
            disable_notification=False,
        )

        create_date = "хз"
        if payment is not None:
            create_date = payment.created.strftime("%H:%M:%S")

        pay_date = "хз"
        if qiwi_payment is not None:
            pay_date = qiwi_payment.date.strftime("%H:%M:%S")

        await self.bot.send_message(
            self.config.admins_chat,
            admins_profit_text.format(
                profit_link=outs_msg.url,
                service=self.SERVICE_NAMES[profit.service],  # refactor
                amount=profit.amount,
                share=profit.share,
                mention=mention,
                moll=int(profit.share / profit.amount),
                create_date=create_date,
                pay_date=pay_date,
            ),
            disable_notification=False,
        )
