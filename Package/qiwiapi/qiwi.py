from .types import Payments
from .api import Api


class Qiwi(Api):
    async def check(self, on_payments: callable):
        if self.last_transactions is None:
            self.last_transactions = await self.get_transactions(rows=15)

        if self.last_transactions.data:
            transactions = await self.get_transactions(rows=15)
            for i, transaction in enumerate(transactions.data):
                if transaction.txnId == self.last_transactions.data[0].txnId and i != 0:
                    # new transactions
                    await on_payments(
                        Payments(
                            data=transactions.data[:i],
                            nextTxnId=transactions.nextTxnId,
                            nextTxnDate=transactions.nextTxnDate,
                        ),
                    )
                    self.last_transactions = transactions  # update transactions
                    break

    @classmethod  # get currency as string
    def get_currency(cls, currency: int) -> str:
        return (
            "RUB"
            if currency == 643
            else "USD"
            if currency == 840
            else "KZT"
            if currency == 398
            else "ХЗ"
        )

    @classmethod  # get level as string
    def get_identification_level(cls, level: str) -> str:
        return (
            "Основной"
            if level == "SIMPLE" or level == "VERIFIED"
            else "Профессиональный"
            if level == "FULL"
            else "Без верификации"
        )
