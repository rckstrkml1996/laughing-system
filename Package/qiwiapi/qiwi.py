import re

from .types import Payments
from .api import Api


class Qiwi(Api):
    RUB_CURRENCY = 643
    USD_CURRENCY = 840
    KZT_CURRENCY = 398

    LEVEL_NONVERIFS = ["ANONYMOUS"]  # without verif
    LEVEL_MAINS = ["SIMPLE", "VERIFIED"]  # simple status
    LEVEL_FULLS = ["FULL"]  # fullverif status

    def __init__(
        self,
        token: str,
        proxy_url: str = None,
        validate: bool = True,
        on_invalid_proxy: callable = None,
    ):
        self.validate_proxy = False

        if validate:
            self.validate(token, proxy_url)
            if proxy_url is not None:
                self.validate_proxy = True

        super().__init__(token, proxy_url, self.validate_proxy, on_invalid_proxy)

    @classmethod
    def validate(cls, token: str, proxy_url: str = None):
        if not re.fullmatch(r"[a-fA-F\d]{32}", token):
            raise ValueError(
                f"Token must be 32 len, and match [a-fA-F\d] regexp, not '{token}'"
            )
        if proxy_url is not None:
            regexp = (
                r"(http|https):\/\/(.+):(.+)@(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):(\d+)"
            )
            if not re.fullmatch(regexp, proxy_url):
                raise ValueError(
                    f"Proxy must match {regexp}, '{proxy_url}' - does not match!"
                )

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

    @classmethod
    def get_currency(cls, currency: int) -> str:
        """get currency as string"""
        return (
            "RUB"
            if currency == cls.RUB_CURRENCY
            else "USD"
            if currency == cls.USD_CURRENCY
            else "KZT"
            if currency == cls.KZT_CURRENCY
            else "ХЗ"
        )

    @classmethod
    def get_identification_level(cls, level: str) -> str:
        """get level as string"""
        return (
            "Основной"
            if level in cls.LEVEL_MAINS
            else "Профессиональный"
            if level in cls.LEVEL_FULLS
            else "Анонимус"
        )
