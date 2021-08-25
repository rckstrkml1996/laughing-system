from asyncio import sleep

from customutils.models import CasinoPayment
from customutils.qiwiapi import QiwiPaymentsParser, QiwiApi
from customutils.qiwiapi.types import Payments
from loguru import logger

from config import config


async def on_new_payment(api: QiwiApi, payments: Payments):
    logger.info(f"New payments {len(payments.data)} notify.")
    headers = {
        "Authorization": f"Bearer {api.token}",
        "Content-Type": "application/json",
    }
    for transaction in payments.data:
        status = "Blank"
        try:
            pay = CasinoPayment.get(comment=transaction.comment)
            status = "Comment"
            if (
                transaction.trnsType == "IN"
                and pay.amount <= transaction.transactionSum.amount
            ):
                status = "InComAmount"
                logger.debug(
                    f"there are payment with good amount {pay.amount} and comment."
                )
                if transaction.transactionSum.currency == 643:
                    status = "InDone"
                    pay.done = True
                    pay.save()
                    logger.info("There are good payment, done in base.")
        except CasinoPayment.DoesNotExist:
            logger.debug(f"Payment with comment {transaction.comment} not in base!")

        await api.session.post(
            config("new_transaction_url"),
            params={"status": status},
            headers=headers,
            data=transaction.json(by_alias=True),
        )
        await api.close()

        print(status)


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
