from asyncio import sleep
from typing import Union, Optional

from aiogram import Bot
from aiogram.types import InputFile
from loguru import logger

from qiwiapi import Qiwi
from qiwiapi.exceptions import InvalidProxy
from qiwiapi.types import Transaction
from customutils import BotsConfig
from models import (
    Worker,
    Profit,
    QiwiPayment,
    CasinoPayment,
    EscortPayment,
    TradingPayment,
)
from data.texts import (
    chat_profit_text,
    outs_profit_text,
    admins_profit_text,
    invalid_proxy_text,
)
from utils.render import render_profit
from utils import basefunctional


class PayChecker:
    SERVICE_NAMES = ["Казино", "Эскорт", "Трейдинг", "Прямой перевод"]

    def __init__(self, bot: Bot, config: BotsConfig):
        if not isinstance(bot, Bot):
            raise TypeError(
                f"Argument 'bot' must be an instance of Bot, not '{type(bot).__name__}'"
            )

        self.bot = bot
        self.config = config

        self._qiwi = None
        self._working = False

    def work(self):
        self._working = True
        logger.debug("PayChecker working.")

    def stop(self):
        self._working = False

    async def check_casino(self, transaction: Transaction) -> Optional[CasinoPayment]:
        if transaction.sum.currency == Qiwi.RUB_CURRENCY:
            try:
                return CasinoPayment.get(
                    comment=transaction.comment
                )  # maybe implement created > -14 days?
            except CasinoPayment.DoesNotExist:
                pass

    async def check_transaction(self, transaction: Transaction):
        casino = self.check_casino(transaction)
        if casino:
            print(f"its {casino}")
            return  # return send_profit(profit)

        # escort = self.check_escort(transaction)
        # if escort:
        #     print(f"its {escort}")
        #     return

    async def start(self):
        self.work()

        while self._working:
            logger.debug(f"PayChecker check {self._qiwi}")
            if self._qiwi is None and isinstance(self.config.qiwi_tokens, list):
                self._qiwi = Qiwi(**self.config.qiwi_tokens[0])

            try:
                await self._qiwi.check_payments(
                    self.check_transaction, rows=15, operation=self._qiwi.IN
                )
            except InvalidProxy:
                await self.bot.send_message(
                    self.config.admins_chat,
                    invalid_proxy_text.format(token=self._qiwi.token),
                )

            await sleep(self.config.qiwi_check_time, int)

        # await self.bot.session.close() # if using outside executor

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
        profit.msg_url = outs_msg.url
        profit.save()

        if self.config.profit_sticker_id is not None:
            await self.bot.send_sticker(  # try: except:
                self.config.workers_chat, self.config.profit_sticker_id
            )
        await self.bot.send_message(  # send info about profit in workers chat
            self.config.workers_chat,
            chat_profit_text.format(
                profit_link=profit.msg_url,
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
                profit_link=profit.msg_url,
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
