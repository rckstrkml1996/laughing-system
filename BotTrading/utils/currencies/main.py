import os
import json
from json import JSONDecodeError
from asyncio import sleep

from loguru import logger

from .messari import MessariApi


class NoCurrenciesError(Exception):
    pass


class CurrencyWorker(MessariApi):
    FILE_PATH = "currencies.json"

    def __init__(self):
        self.convertion = 75  # rub
        self.currencies = []
        self._working = False
        self.restrict_json()

    def save_json(self):
        with open(self.FILE_PATH, "w") as f:
            json.dump(
                {"convertion": self.convertion, "currencies": self.currencies},
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
                self.convertion = settings.get("convertion", self.convertion)
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

    def update_price(self, currency_id: int, price_usd: int, price_rub: int):
        self.currencies[currency_id]["price_usd"] = price_usd
        self.currencies[currency_id]["price"] = price_rub  # rub
        self.save_json()

    async def start_work(self):
        self._working = True
        while self._working:
            for curr_id, currency in enumerate(self.currencies):
                try:
                    price_usd = await self.get_market_price(currency["symbol"])
                    price_rub = self.convertion * price_usd
                    self.update_price(curr_id, round(price_usd, 2), round(price_rub, 2))
                except Exception as ex:
                    logger.error(ex)
                await sleep(2)
            await sleep(60)

    def stop_work(self):
        self._working = False
