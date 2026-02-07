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
    def __init__(
        self,
        token: str,
        wallet: str = None,
        proxy_url: str = None,
        check_proxy: bool = False,
        on_invalid_proxy: callable = None,
    ):
        """
        param: token - qiwi api authorization token
        param: proxy_url - proxy url
        param: check_proxy - if true, checking proxy!
        param: on_invalid_proxy(qiwi: Qiwi) - callable that calls when InvalidProxy
        """

        self.token = token
        self.wallet = wallet
        self.proxy = proxy_url  # only http or https proxy.
        self.validate_proxy = check_proxy
        self.on_invalid_proxy = on_invalid_proxy

        self.profile = None
        self._session: aiohttp.ClientSession = None
        self.headers = {"authorization": "Bearer " + token}

    async def get_profile(self):
        if self.profile is None:
            self.profile = await self.get_new_profile()

        return self.profile

    async def get_new_profile(self) -> Profile:
        url = "https://edge.qiwi.com/person-profile/v1/profile/current"

        response = await self.session.get(url, proxy=self.proxy, ssl=False)
        if response.status == 401:
            raise InvalidToken
        elif response.status == 403:
            raise InvalidAccount
        elif response.status != 200:
            raise UnexpectedResponse

        json = await response.json()
        await self.close()

        return Profile(**json)

    def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(5),
            trust_env=True,
            headers=self.headers,
        )

    @property  # WARN DEPRECATED
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

    async def get_accounts(self) -> Accounts:
        if self.wallet is None:
            profile = await self.get_profile()
            self.wallet = profile.contractInfo.contractId

        url = f"https://edge.qiwi.com/funding-sources/v2/persons/{self.wallet}/accounts"

        response = await self.session.get(url, proxy=self.proxy, ssl=False)
        if response.status == 401:
            raise InvalidToken
        elif response.status == 403:
            raise InvalidAccount
        elif response.status != 200:
            raise UnexpectedResponse

        json = await response.json()
        await self.close()

        return Accounts(**json).accounts

    async def get_payments(self, rows: int = 50, operation: str = "ALL") -> Payments:
        if self.wallet is None:
            profile = await self.get_profile()
            self.wallet = profile.contractInfo.contractId

        url = f"https://edge.qiwi.com/payment-history/v2/persons/{self.wallet}/payments"

        response = await self.session.get(
            url,
            params={"rows": rows, "operation": operation},
            proxy=self.proxy,
            ssl=False,
        )
        if response.status == 401:
            raise InvalidToken
        elif response.status == 403:
            raise InvalidAccount
        elif response.status != 200:
            raise UnexpectedResponse

        json = await response.json()
        await self.close()

        return Payments(**json)

    async def get_payments_total(
        self,
        startDate: Union[str, datetime],
        endDate: Union[str, datetime],
        operation: str = "ALL",
        time_zone: str = "+03:00",
    ) -> TotalPayments:
        """datetime with tzinfo!!!"""
        if isinstance(startDate, datetime):
            start_date = startDate.strftime("%Y-%m-%dT%H:%M:%S") + str(time_zone)
            if startDate.tzinfo:
                start_date = start_date[:-2] + ":" + start_date[-2:]
        else:
            start_date = startDate

        if isinstance(endDate, datetime):
            end_date = endDate.strftime("%Y-%m-%dT%H:%M:%S") + str(time_zone)
            if endDate.tzinfo:
                end_date = end_date[:-2] + ":" + end_date[-2:]
        else:
            end_date = endDate

        if self.wallet is None:
            profile = await self.get_profile()
            self.wallet = profile.contractInfo.contractId

        url = f"https://edge.qiwi.com/payment-history/v2/persons/{self.wallet}/payments/total"

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
        await self.close()

        return TotalPayments(**json)

    async def made_payments(
        self, account: str, amount, currency="643", comment=None
    ) -> PaymentInfo:
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
        await self.close()

        try:
            return PaymentInfo(**json)
        except ValidationError:
            return json

    async def check_proxy(
        self, timeout: int = 3, url: str = "https://example.com"
    ) -> bool:
        if self.proxy is None:
            return True
        session = aiohttp.ClientSession()
        answer = True
        try:
            await session.get(url, proxy=self.proxy, ssl=False, timeout=timeout)
        except TimeoutError:
            answer = False
        except ClientProxyConnectionError:
            answer = False
        except ClientHttpProxyError:
            answer = False
        finally:
            await session.close()
        return answer

    async def close(self):  # WARN DEPRECATED
        session = self.session
        if session is not None and not session.closed:
            await session.close()
