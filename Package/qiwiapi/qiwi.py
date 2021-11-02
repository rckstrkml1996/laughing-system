import re
from asyncio import sleep

from .api import Api


class Qiwi(Api):
    ALL = "ALL"
    OUT = "OUT"
    IN = "IN"
    QIWI_CARD = "QIWI_CARD"

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
        self.last_payments = None  # []

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

    async def check_payments(
        self, on_transaction: callable, rows: int = 15, operation: str = "ALL"
    ):
        """Check if new payments"""
        payments = await self.get_payments(rows=rows, operation=operation)
        if self.last_payments is None:
            self.last_payments = payments

        # print(
        #     len(payments.data),
        #     len(self.last_payments.data),
        #     payments.data[0].txnId,
        #     self.last_payments.data[0].txnId,
        # )  # debugging

        last_txnid = self.last_payments.data[0].txnId

        if payments.data[0].txnId != last_txnid:
            for transaction in filter(lambda p: p.txnId > last_txnid, payments.data):
                await on_transaction(transaction)
                await sleep(0.05)

        self.last_payments = payments

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
