from asyncio import sleep
from asyncio.exceptions import TimeoutError
from configparser import NoOptionError

from loguru import logger
from aiohttp.client_exceptions import ClientProxyConnectionError
from aiogram.types.input_file import InputFile
from customutils.models import QiwiPayment, Profit, CasinoPayment
from customutils.qiwiapi import QiwiPaymentsParser
from customutils.qiwiapi.types import Payments, Transaction

from loader import dp, db_commands
from config import config, ServiceNames
from data import payload
from utils.executional import get_api, delete_api_proxy
from .render import render_profit


async def check_casino(traction: Transaction):
    try:
        pay = CasinoPayment.get(comment=traction.comment)

        if traction.trnsType == "IN" and pay.amount <= traction.transactionSum.amount:
            logger.debug(f"Some payment with {pay.amount} amount")
            if traction.transactionSum.currency == 643:
                pay.done = True
                pay.save()
                logger.info(
                    f"Apply payment {pay.amount} amount in base and making pay."
                )

                casino_user = pay.owner
                worker = casino_user.owner

                service = ServiceNames[0]  # thats casino

                username = worker.username
                amount = int(pay.amount)

                moll = 0.8 if casino_user.fuckedup else 0.7
                share = int(pay.amount * moll)

                qiwi_pay = QiwiPayment.create(
                    person_id=traction.personId,
                    account=traction.account,
                    amount=traction.total.amount,
                    currency=traction.total.currency,
                    comment=traction.comment,
                    date=traction.date,
                )
                Profit.create(
                    owner=worker,
                    amount=amount,
                    share=share,
                    service=service,
                    payment=qiwi_pay,
                )
                logger.debug("Sucessfully created QiwiPayment and Profit in base.")

                all_profit = db_commands.get_profits_sum(worker.id)
                profit_path = render_profit(
                    all_profit, amount, share, service, username
                )
                logger.debug(
                    f"Succesfully rendered profit path: {profit_path}, sending to outs chat"
                )
                await dp.bot.send_photo(
                    config("outs_chat"),
                    InputFile(profit_path),
                    caption=payload.profit_text.format(
                        service=service,
                        share=share,
                        amount=amount,
                        cid=worker.cid,
                        name=worker.username if worker.username else worker.name,
                    ),
                )
                logger.debug("Succesfully sent to outs and admins chat")
                return True
    except CasinoPayment.DoesNotExist:
        logger.debug(f"Payment with comment {traction.comment} not in base!")
    return False


async def on_new_payment(payments: Payments):
    logger.info(f"On new payments {len(payments.data)} notify.")
    for transaction in payments.data:
        if await check_casino(transaction):  # check if supply on casino
            print("casino payment parse as qiwi chilen")
        else:
            print("blanck payment epta")


async def check_payments():
    try:
        token = config("qiwi_tokens")
        if isinstance(token, list):
            token = token[0]

        api, proxy_url = get_api(token)  # get api instance by token(proxy) string
        parser = QiwiPaymentsParser(api, on_new_payment)
    except NoOptionError:
        token = None

    logger.debug("QiwiPaymentsParser started succesfully.")
    while True:
        try:
            new_token = config("qiwi_tokens")
            if isinstance(new_token, list):
                new_token = new_token[0]

            if new_token != token:
                token = new_token
                api, proxy_url = get_api(token)
                parser = QiwiPaymentsParser(api, on_new_payment)
                logger.info(f"Parsing payments with new qiwi {token}")

            try:
                await parser.check()
            except (ClientProxyConnectionError, TimeoutError):
                delete_api_proxy(token)
                await parser.api.close()
        except NoOptionError:
            token = None

        await sleep(60)
