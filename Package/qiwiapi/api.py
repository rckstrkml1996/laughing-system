from time import time
from datetime import datetime
from asyncio.exceptions import TimeoutError
from typing import Union

import aiohttp
from aiohttp.client_exceptions import ClientProxyConnectionError, ClientHttpProxyError
from pydantic.error_wrappers import ValidationError

from .exceptions import InvalidToken, InvalidAccount, UnexpectedResponse, InvalidProxy
from .types import Accounts, TotalPayments, Payments, PaymentInfo, Profile


class Api:
    """
    Манипуляции напрямую с Qiwi API
    """

    def __init__(self, token: str, proxy_url: str = None, check_proxy: bool = False):
        self.token = token
        self.proxy = proxy_url  # only http or https proxy.
        # self.proxy_auth = aiohttp.BasicAuth("3n4bvPyg", "B6NCe3Bji")
        self.validate_proxy = check_proxy
        self.profile = None
        self._session: aiohttp.ClientSession = None
        self.headers = {"authorization": "Bearer " + token}

    async def get_profile(self):
        if self.profile is None:
            await self.get_new_profile()
        return self.profile

    async def get_new_profile(self):
        url = "https://edge.qiwi.com/person-profile/v1/profile/current"

        response = await self.session.get(url, proxy=self.proxy, ssl=False)
        if response.status == 401:
            raise InvalidToken
        elif response.status == 403:
            raise InvalidAccount
        elif response.status != 200:
            raise UnexpectedResponse

        json = await response.json()

        self.profile = Profile(**json)
        return self.profile

    def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False),
            timeout=aiohttp.ClientTimeout(5),
            trust_env=True,
            headers=self.headers,
        )

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

    async def get_balance(self):
        if self.validate_proxy:
            if not await self.check_proxy():
                raise InvalidProxy(f"'{self.proxy}' is invalid!")

        profile = await self.get_profile()
        url = f"https://edge.qiwi.com/funding-sources/v2/persons/{profile.contractInfo.contractId}/accounts"

        response = await self.session.get(url, proxy=self.proxy, ssl=False)
        if response.status == 401:
            raise InvalidToken
        elif response.status == 403:
            raise InvalidAccount
        elif response.status != 200:
            raise UnexpectedResponse

        json = await response.json()

        return Accounts(**json).accounts

    async def get_transactions(self, rows: int = 50):
        profile = await self.get_profile()
        wallet = profile.contractInfo.contractId
        url = f"https://edge.qiwi.com/payment-history/v2/persons/{wallet}/payments"

        response = await self.session.get(
            url, params={"rows": rows}, proxy=self.proxy, ssl=False
        )
        if response.status == 401:
            raise InvalidToken
        elif response.status == 403:
            raise InvalidAccount
        elif response.status != 200:
            raise UnexpectedResponse

        json = await response.json()

        return Payments(**json)

    async def get_statistics(
        self,
        startDate: Union[str, datetime],
        endDate: Union[str, datetime],
        operation: str = "ALL",
    ):
        if isinstance(startDate, datetime):
            start_date = startDate.strftime("%Y-%m-%dT%H:%M:%S%z")
            if startDate.tzinfo:
                start_date = start_date[:-2] + ":" + start_date[-2:]
        else:
            start_date = startDate

        if isinstance(endDate, datetime):
            end_date = endDate.strftime("%Y-%m-%dT%H:%M:%S%z")
            if endDate.tzinfo:
                end_date = end_date[:-2] + ":" + end_date[-2:]
        else:
            end_date = endDate

        profile = await self.get_profile()
        wallet = profile.contractInfo.contractId
        url = (
            f"https://edge.qiwi.com/payment-history/v2/persons/{wallet}/payments/total"
        )

        params = {
            "startDate": start_date,
            "endDate": end_date,
            "operation": operation,
        }

        response = await self.session.get(
            url, params=params, proxy=self.proxy, ssl=False
        )
        if response.status == 401:
            raise InvalidToken
        elif response.status == 403:
            raise InvalidAccount
        elif response.status != 200:
            raise UnexpectedResponse

        json = await response.json()

        return TotalPayments(**json)

    async def pay(self, account: str, amount, currency="643", comment=None):
        url = "https://edge.qiwi.com/sinap/api/v2/terms/99/payments"

        params = {
            "id": self._transaction_id,
            "sum": {"amount": amount, "currency": currency},
            "paymentMethod": {"type": "Account", "accountId": "643"},
            "comment": comment,
            "fields": {"account": account},
        }

        response = await self.session.post(
            url, json=params, proxy=self.proxy, ssl=False
        )
        if response.status == 401:
            raise InvalidToken
        elif response.status == 403:
            raise InvalidAccount
        elif response.status != 200:
            raise UnexpectedResponse

        json = await response.json()

        try:
            return PaymentInfo(**json)
        except ValidationError:
            return json

    async def check_proxy(self, url: str = "https://qiwi.com"):
        answer = True
        try:
            await self.session.get(url, proxy=self.proxy, ssl=False)
        except TimeoutError:  # this is for different log
            answer = False
        except ClientProxyConnectionError:
            answer = False  # this is for different log
        except ClientHttpProxyError:
            answer = False

        return answer

    async def close(self):
        session = self.session  # bugfix
        if session is not None:
            await session.close()
