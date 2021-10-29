from .types import Payments


class QiwiPaymentsParser:
    def __init__(self, qiwi_api, notify: callable):
        self.api = qiwi_api
        self.last_transactions = None
        self.notify: callable = notify

    async def check(self):
        if self.last_transactions is None:
            self.last_transactions = await self.api.get_transactions(rows=15)

        if self.last_transactions.data:
            transactions = await self.api.get_transactions(rows=15)
            for i, transaction in enumerate(transactions.data):
                if transaction.txnId == self.last_transactions.data[0].txnId and i != 0:
                    # new transactions
                    await self.notify(
                        Payments(
                            data=transactions.data[:i],
                            nextTxnId=transactions.nextTxnId,
                            nextTxnDate=transactions.nextTxnDate,
                        ),
                    )
                    self.last_transactions = transactions  # update transactions
                    break
