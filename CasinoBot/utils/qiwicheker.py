from asyncio import sleep

from customutils.qiwiapi import QiwiPaymentsParser, QiwiApi
from customutils.qiwiapi.types import Payments

from config import config


async def new_payments(payments: Payments):
    print("new_payments notifyed")


async def check_payments():
    token = config("qiwi_tokens")
    if isinstance(token, list):
        token = token[0]
    api = QiwiApi(token)
    parser = QiwiPaymentsParser(api)

    while True:
        new_token = config("qiwi_tokens")
        if isinstance(new_token, list):
            new_token = new_token[0]

        if new_token != token:
            token = new_token
            api = QiwiApi(token)
            parser = QiwiPaymentsParser(api, new_payments)
            print("new qiwitoken epta")

        await parser.check()

        await sleep(60)
