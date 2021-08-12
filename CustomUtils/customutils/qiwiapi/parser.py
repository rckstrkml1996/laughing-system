import asyncio

from .types import Payments


class QiwisPaymentChecker:
    def __init__(self, qiwiapi_list, loop=None):
        self.loop = loop
        if loop is None:
            self.loop = asyncio.get_event_loop()
        self.qiwi_parsers = []
        self.qiwis = qiwiapi_list

    async def start(self):
        for qiwi in self.qiwis:
            self.qiwi_parsers.append(QiwiPaymentsParser(qiwi))

        tasks = []
        for parser in self.qiwi_parsers:
            tasks.append(self.loop.create_task(parser.start()))

        await asyncio.gather(*tasks)


class QiwiPaymentsParser:
    def __init__(self, qiwi_api):
        self.api = qiwi_api
        self.last_transactions = None
        self.url = "http://127.0.0.1:8000/new_payments"

    async def start(self):
        self.last_transactions = await self.api.get_transactions(rows=15)
        while True:
            transactions = await self.api.get_transactions(rows=15)
            for i, transaction in enumerate(transactions.data):
                if transaction.txnId == self.last_transactions.data[1].txnId:
                    if i != 0:
                        # new transactions
                        headers = {"Authorization": f"Bearer {self.api.TOKEN}",
                                   'content-type': 'application/json'}
                        await self.api.session.post(
                            self.url,
                            headers=headers,
                            data=Payments(
                                data=transactions.data[:i],
                                nextTxnId=transactions.nextTxnId,
                                nextTxnDate=transactions.nextTxnDate,
                            ).json(by_alias=True)
                        )
                        print(1)
                        # print(Payments(
                        #     data=transactions.data[:i],
                        #     nextTxnId=transactions.nextTxnId,
                        #     nextTxnDate=transactions.nextTxnDate,
                        # ).dict(by_alias=True))
                    self.last_transactions = transactions  # update transactions
            await asyncio.sleep(100)  # 1.66 minuts
