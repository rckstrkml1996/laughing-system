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
    unmatched_payment_text,
)
from data.keyboards import profit_pay_keyboard
from utils.render import render_profit
from utils import basefunctional


class PayChecker:
    """
    Qiwi Payments Checker, by tg: @ukhide :)
    """

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
        logger.debug("PayChecker start working!")

    def stop(self):
        self._working = False
        logger.debug("PayChecker stop working!")

    async def filter_casino(self, transaction: Transaction) -> Optional[CasinoPayment]:
        if transaction.sum.currency == Qiwi.RUB_CURRENCY:
            try:
                payment = CasinoPayment.get(
                    comment=transaction.comment
                )  # maybe implement created > -14 days?
                if transaction.sum.amount >= payment.amount:
                    return payment
            except CasinoPayment.DoesNotExist:
                pass

    async def on_new_transaction(self, transaction: Transaction):
        logger.info(
            f"New Qiwi transaction: #{transaction.txnId}, "
            f"{transaction.sum.amount} ({transaction.sum.currency}), "
            f"{transaction.comment}"
        )

        qiwi_payment = QiwiPayment.create(
            person_id=transaction.personId,
            account=transaction.account,
            amount=transaction.sum.amount,
            payment_type=transaction.trnsType,
            currency=transaction.sum.currency,
            comment=transaction.comment,
            date=transaction.date,
        )

        if transaction.trnsType == Qiwi.IN:
            payment = await self.filter_casino(transaction)
            if payment is not None:
                payment.done = 1
                payment.save()

                pay_count = basefunctional.get_payments_count(
                    CasinoPayment, payment.owner
                )

                share = transaction.sum.amount * 0.8 if pay_count == 1 else 0.7
                await self.send_profit(
                    Profit.create(
                        owner=payment.owner.owner,
                        service_id=0,  # casino,
                        service_name=f"Казино Х{pay_count}",
                        payment=qiwi_payment,
                        amount=transaction.sum.amount,
                        share=int(share),  # then as int in base!
                    ),
                    payment,
                )
        else:
            self.bot.send_message(
                self.config.admins_chat,
                unmatched_payment_text.format(
                    qiwi_id=dict(
                        filter(
                            lambda q: q["token"] == self._qiwi.token,
                            self.config.qiwi_tokens,
                        )
                    ).get(self._qiwi.token),
                    amount=transaction.sum.amount,
                    currency=Qiwi.get_currency(transaction.sum.currency),
                ),
            )

    async def start(self):
        self.work()

        while self._working:
            logger.debug(f"PayChecker check qiwi={self._qiwi}")
            if self._qiwi is None and isinstance(self.config.qiwi_tokens, list):
                self._qiwi = Qiwi(**self.config.qiwi_tokens[0])

            try:
                await self._qiwi.check_payments(
                    self.on_new_transaction, rows=15, operation=Qiwi.ALL
                )
            except InvalidProxy:
                await self.bot.send_message(
                    self.config.admins_chat,
                    invalid_proxy_text.format(token=self._qiwi.token),
                )

            await sleep(self.config.qiwi_check_time)

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
            profit.service_name,
            worker.username,
            "... work ...",  # analog text
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
                service=profit.service_name,  # refactor
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
                service=profit.service_name,  # refactor
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
                service=profit.service_name,  # refactor
                amount=profit.amount,
                share=profit.share,
                moll=int(profit.share / profit.amount),
                mention=mention,
                create_date=create_date,
                pay_date=pay_date,
            ),
            reply_markup=profit_pay_keyboard(profit.id),
            disable_notification=False,
        )
