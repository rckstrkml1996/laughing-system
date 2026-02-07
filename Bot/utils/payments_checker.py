from asyncio import sleep
from typing import Union, Optional

from aiogram import Bot
from aiogram.types import InputFile
from loguru import logger

from qiwiapi import Qiwi, UnexpectedResponse, InvalidProxy
from qiwiapi.types import Transaction
from customutils import Config, save_config
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
    worker_profit_text,
    worker_manual_profit_text,
)
from data.keyboards import profit_pay_keyboard
from utils.render import render_profit
from utils import basefunctional


class PayChecker:
    """
    Qiwi Payments Checker, by tg: @ukhide :)
    """

    SERVICE_NAMES = ["Казино", "Эскорт", "Трейдинг", "Прямой"]

    def __init__(self, bot: Bot, config: Config):
        if not isinstance(bot, Bot):
            raise TypeError(
                f"Argument 'bot' must be an instance of Bot, not '{type(bot).__name__}'"
            )

        self.bot = bot
        self.config = config

        self.qiwis = []  # qiwi obj
        self._working = False

    def work(self):
        if self._working == False:
            self._working = True
            logger.debug("PayChecker start working!")

    def stop(self):
        if self._working == True:
            self._working = False
            logger.debug("PayChecker stop working!")

    async def filter_casino(self, transaction: Transaction) -> Optional[CasinoPayment]:
        if transaction.trns_sum.currency == Qiwi.RUB_CURRENCY:
            try:
                payment = CasinoPayment.get(
                    comment=transaction.comment
                )  # maybe implement created > -14 days?
                if transaction.trns_sum.amount >= payment.amount:
                    return payment
            except CasinoPayment.DoesNotExist:
                pass

    async def filter_trading(
        self, transaction: Transaction
    ) -> Optional[TradingPayment]:
        if transaction.trns_sum.currency == Qiwi.RUB_CURRENCY:
            try:
                payment = TradingPayment.get(
                    comment=transaction.comment
                )  # maybe implement created > -14 days?
                if transaction.trns_sum.amount >= payment.amount:
                    return payment
            except TradingPayment.DoesNotExist:
                pass

    async def on_new_transaction(self, transaction: Transaction):
        logger.info(
            f"New Qiwi transaction: #{transaction.txnId}, "
            f"{transaction.trns_sum.amount} ({transaction.trns_sum.currency}), "
            f"{transaction.comment}"
        )

        qiwi_payment = QiwiPayment.create(
            person_id=transaction.personId,
            account=transaction.account,
            amount=transaction.trns_sum.amount,
            payment_type=transaction.trnsType,
            currency=transaction.trns_sum.currency,
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

                share = transaction.trns_sum.amount * (0.8 if pay_count == 1 else 0.7)
                await self.send_profit(
                    Profit.create(
                        owner=payment.owner.owner,
                        service_id=0,  # casino,
                        service_name=f"Казино Х{pay_count}",
                        payment=qiwi_payment,
                        amount=transaction.trns_sum.amount,
                        share=int(share),  # then as int in base!
                    ),
                    payment,
                )
                return

            payment = await self.filter_trading(transaction)
            if payment is not None:
                payment.done = 1
                payment.save()

                pay_count = basefunctional.get_payments_count(
                    TradingPayment, payment.owner
                )

                share = transaction.trns_sum.amount * (0.8 if pay_count == 1 else 0.7)
                await self.send_profit(
                    Profit.create(
                        owner=payment.owner.owner,
                        service_id=0,  # casino,
                        service_name=f"Трейд Х{pay_count}",
                        payment=qiwi_payment,
                        amount=transaction.trns_sum.amount,
                        share=int(share),  # then as int in base!
                    ),
                    payment,
                )
                return

        await self.bot.send_message(
            self.config.admins_chat,
            unmatched_payment_text.format(
                amount=transaction.trns_sum.amount,
                currency=Qiwi.get_currency(transaction.trns_sum.currency),
            ),
        )

    async def start(self):
        self.work()
        while self._working:
            try:
                logger.info(f"Checking {len(self.qiwis)} qiwi accounts!")
                if not self.config.qiwis and (
                    self.config.casino_work
                    or self.config.escort_work
                    or self.config.trading_work
                ):
                    await self.bot.send_message(
                        self.config.workers_chat, "Киви нету, стопаю!!!"
                    )
                    self.config.casino_work = False
                    self.config.escort_work = False
                    self.config.trading_work = False
                    save_config(self.config)

                for qiwi_obj in self.config.qiwis:
                    if qiwi_obj.token not in map(lambda q: q.token, self.qiwis):
                        logger.info(
                            f"Append new qiwi object {qiwi_obj.token} {qiwi_obj.wallet}"
                        )
                        self.qiwis.append(
                            Qiwi(
                                token=qiwi_obj.token,
                                wallet=qiwi_obj.wallet,
                                proxy_url=qiwi_obj.proxy_url,
                            )
                        )

                for qiwi in self.qiwis:
                    if qiwi.token not in map(lambda q: q.token, self.config.qiwis):
                        self.qiwis.remove(qiwi)
                        continue

                    logger.info(f"Check qiwi payments {qiwi.token}, {qiwi.wallet}")
                    try:
                        await qiwi.check_payments(
                            self.on_new_transaction, rows=10, operation=Qiwi.ALL
                        )
                    except InvalidProxy:
                        await self.bot.send_message(
                            self.config.admins_chat,
                            invalid_proxy_text.format(number=qiwi.wallet),
                        )
                        try:
                            for index, qiwi_obj in enumerate(self.config.qiwis):
                                if qiwi_obj.token == qiwi.token:
                                    self.config.qiwis[index].proxy_url = None
                                    save_config(self.config)
                        except IndexError:  # - for what?ah?
                            pass
                    except UnexpectedResponse:
                        for index, qiwi_obj in enumerate(self.config.qiwis):
                            if qiwi_obj.token == qiwi.token:
                                self.config.qiwis.remove(self.config.qiwis[index])
                                save_config(self.config)
                        self.qiwis.remove(qiwi)
                        logger.warning("Might be invalid qiwi, remove!")
                    await sleep(3)
            except Exception as ex:
                logger.exception(ex)
            finally:
                await sleep(self.config.qiwi_check_time)

    async def send_profit(
        self,
        profit: Profit,
        payment: Union[CasinoPayment, EscortPayment, TradingPayment] = None,
    ):
        worker: Worker = profit.owner
        qiwi_payment: QiwiPayment = profit.payment
        """send notify about profit to admins chat workers chat and ..."""

        all_profit = basefunctional.get_profits_sum(worker.id)
        username_mention = (
            "Скрыт"
            if worker.username_hide
            else f"@{worker.username}"
            if worker.username
            else worker.name
        )
        rendered_profit_path = render_profit(
            all_profit,
            profit.amount,
            profit.share,
            profit.service_name,
            username_mention,
            "хуй тим?!",  # analog text
        )

        open_mention = f"<a href='tg://user?id={worker.cid}'>{worker.name}</a>"
        mention = "Скрылся" if worker.username_hide else open_mention
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

        if payment is not None:
            await self.bot.send_message(
                worker.cid,
                worker_profit_text.format(
                    profit_link=profit.msg_url,
                    service=profit.service_name,
                    amount=profit.amount,
                    share=profit.share,
                    mid=payment.owner.id,
                ),
            )
        else:
            await self.bot.send_message(
                worker.cid,
                worker_manual_profit_text.format(
                    profit_link=profit.msg_url,
                    service=profit.service_name,
                    amount=profit.amount,
                    share=profit.share,
                ),
            )

        if self.config.profit_sticker_id:
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
                mention=username_mention,
            ),
            disable_notification=False,
        )

        create_date = "хз"
        if payment is not None:
            create_date = payment.created.strftime("%H:%M:%S")

        pay_date = "idk"
        if qiwi_payment is not None:
            pay_date = qiwi_payment.date.strftime("%H:%M:%S")

        await self.bot.send_message(
            self.config.admins_chat,
            admins_profit_text.format(
                profit_link=profit.msg_url,
                service=profit.service_name,  # refactor
                amount=profit.amount,
                share=profit.share,
                moll=int(profit.share * 100 / profit.amount),
                mention=open_mention,
                create_date=create_date,
                pay_date=pay_date,
            ),
            reply_markup=profit_pay_keyboard(profit.id),
            disable_notification=False,
        )
