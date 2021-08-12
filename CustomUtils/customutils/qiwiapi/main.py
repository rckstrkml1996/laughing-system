from time import time

import aiohttp
from pydantic.error_wrappers import ValidationError

from .exceptions import InvalidToken
from .types import Accounts, Payments, PaymentInfo


class QiwiApi:
    """
    Манипуляции напрямую с Qiwi API
    """

    def __init__(self, token: str, account: str):
        self.TOKEN = token
        self.ACCOUNT = account
        self.headers = {"authorization": "Bearer " + token}
        self._session: aiohttp.ClientSession = None

    @property  # <- уже исполниная функция без абьедка
    def session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = self.get_new_session()
        return self._session

    @property
    def _transaction_id(self):
        """
        Generates transaction id for pay() function.
        :return: UNIX time * 1000
        """
        return str(int(time() * 1000))

    def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(headers=self.headers)

    async def get_balance(self):
        url = f"https://edge.qiwi.com/funding-sources/v2/persons/{self.ACCOUNT}/accounts"

        response = await self.session.get(url)
        if response.status == 401:
            raise InvalidToken
        json = await response.json()

        return Accounts(**json).accounts

    async def get_transactions(self, rows: int = 50):
        url = f"https://edge.qiwi.com/payment-history/v2/persons/{self.ACCOUNT}/payments"

        response = await self.session.get(url, params={"rows": rows})
        if response.status == 401:
            raise InvalidToken
        json = await response.json()

        return Payments(**json)

    async def pay(self, account: str, amount, currency="643", comment=None):
        url = "https://edge.qiwi.com/sinap/api/v2/terms/99/payments"

        params = {
            "id": self._transaction_id,
            "sum": {
                "amount": amount,
                "currency": currency
            },
            "paymentMethod": {
                "type": "Account",
                "accountId": "643"
            },
            "comment": comment,
            "fields": {
                "account": account
            }
        }

        response = await self.session.post(url, json=params)
        if response.status == 401:
            raise InvalidToken
        json = await response.json()

        try:
            return PaymentInfo(**json)
        except ValidationError:
            return json

    async def close(self):
        session = self.session  # bugfix
        if session is not None:
            await session.close()
