import re

from .types import Payments
from .api import Api


class Qiwi(Api):
    def __init__(self, token: str, proxy_url: str = None, validate: bool = True):
        self.validate_proxy = False

        if validate:
            if not re.match(r"[a-fA-F\d]{32}", token):
                raise ValueError(
                    "Token must be 32 len, and match [a-fA-F\d] regexp." f"Not {token}"
                )
            if proxy_url is not None:
                self.validate_proxy = True

        super().__init__(token, proxy_url, self.validate_proxy)

    async def check(self, on_payments: callable):
        """Check if new payments"""
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
