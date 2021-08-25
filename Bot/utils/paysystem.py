from asyncio import sleep

from loguru import logger
from customutils.models import QiwiPayment, Profit, CasinoPayment
from customutils.qiwiapi import QiwiPaymentsParser, QiwiApi
from customutils.qiwiapi.types import Payments, Transaction

from loader import db_commands
from config import config, ServiceNames
from .render import render_profit


async def make_profit(all_profit, amount, share, service_name, username):
    profit_path = render_profit(all_profit, amount, share, service_name, username)
    logger.debug(f"Succesfully rendered profit path: {profit_path}")


async def check_casino(traction: Transaction):
    try:
        qiwi_pay = QiwiPayment.create(
            person_id=traction.personId,
            account=traction.account,
            amount=traction.total.amount,
            currency=traction.total.currency,
            comment=traction.comment,
            date=traction.date,
        )
        logger.debug("Sucessfully created QiwiPayment in base.")
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

                service = 0

                username = worker.username
                amount = pay.amount

                all_profit = db_commands.get_profits_sum(worker.id)
                moll = 0.8 if casino_user.fuckedup else 0.7
                share = int(pay.amount * moll)

                Profit.create(
                    owner=worker,
                    amount=amount,
                    share=share,
                    service=service,
                    payment=qiwi_pay,
                )

                await make_profit(
                    all_profit, amount, share, ServiceNames[service], username
                )
    except CasinoPayment.DoesNotExist:
        logger.debug(f"Payment with comment {traction.comment} not in base!")


async def on_new_payment(payments: Payments):
    logger.info(f"On new payments {len(payments.data)} notify.")
    for transaction in payments.data:
        await check_casino(transaction)  # check if supply on casino


async def check_payments():
    token = config("qiwi_tokens")
    if isinstance(token, list):
        token = token[0]
    api = QiwiApi(token)
    parser = QiwiPaymentsParser(api, on_new_payment)

    logger.debug("QiwiPaymentsParser started succesfully.")
    while True:
        new_token = config("qiwi_tokens")
        if isinstance(new_token, list):
            new_token = new_token[0]

        if new_token != token:
            token = new_token
            api = QiwiApi(token)
            parser = QiwiPaymentsParser(api, on_new_payment)
            logger.info(f"Parsing payments with new qiwi {token}")

        await parser.check()
        await sleep(60)
