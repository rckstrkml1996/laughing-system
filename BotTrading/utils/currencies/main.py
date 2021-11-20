import os
import json
from json import JSONDecodeError
from asyncio import sleep

from loguru import logger
from currency_converter import CurrencyConverter

from .messari import MessariApi
from .exceptions import BadRequest, NoCurrenciesError, RateLimit


class CurrencyWorker(MessariApi):
    FILE_PATH = "currencies.json"

    def __init__(self, api_key: str = None):
        self.convertor = CurrencyConverter()
        self.currencies = []
        self._working = False
        self.restrict_json()

        super().__init__(api_key)

    @property
    def convertion(self):
        return self.convertor.convert(1, "USD", "RUB")

    def save_json(self):
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(
                {"currencies": self.currencies},
                f,
                indent=4,
            )

    def restrict_json(self):
        if not os.path.exists(self.FILE_PATH):
            open(self.FILE_PATH, "w").close()  # create file
            raise NoCurrenciesError(
                f"Just created file={self.FILE_PATH}, please, insert values into!"
            )
        try:
            with open(self.FILE_PATH, "r") as f:
                settings = json.load(f)
                self.currencies = settings.get("currencies", None)
                if self.currencies is None:
                    raise NoCurrenciesError(
                        f'file={self.FILE_PATH}, please, insert "currencies" into!'
                    )
        except JSONDecodeError:
            self.save_json()

    async def get_market_price(self, symbol: str) -> int:
        """get usd market price by symbol"""
        response = await self.get_asset_metrics(symbol, "market_data")
        return response["data"]["market_data"]["price_usd"]

    def update_price(self, currency_id: int, price_usd: int):
        self.currencies[currency_id]["price"] = price_usd
        self.save_json()

    def get_currency(self, currency_id: int):
        return self.currencies[currency_id]

    async def start_work(self):
        self._working = True
        while self._working:
            for curr_id, currency in enumerate(self.currencies):
                try:
                    price_usd = await self.get_market_price(currency["symbol"])
                    self.update_price(curr_id, price_usd)
                except RateLimit as ex:
                    logger.error(ex)
                    await sleep(60)
                except BadRequest as ex:
                    logger.error(ex)
                await sleep(1)

            await sleep(500)

    def stop_work(self):
        self._working = False
