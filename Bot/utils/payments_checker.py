from asyncio import sleep

from loguru import logger


class PayChecker:
    def __init__(self, sleep_time: int = 50):
        self._working = False
        self.sleep_time = sleep_time

    async def start(self):
        self._working = True
        logger.debug("QiwiPaymentsParser started.")

        while self._working:
            # if config.qiwi_tokens is not None:
            #     if isinstance(config.qiwi_tokens, list):
            #         new_token = new_token[0] # get last token

            #     if new_token != token:
            #         token = new_token
            #         api, _ = get_api(token)
            #         parser = QiwiPaymentsParser(api, on_new_payment)
            #         logger.info(f"Parsing payments with new qiwi {token}")

            #     try:
            #         await parser.check()
            #         logger.debug(f"Checked qiwi [{parser.api.token}] payments.")
            #     except (ClientProxyConnectionError, TimeoutError):
            #         delete_api_proxy(token)
            #         logger.warning("Deleting Qiwi - Lock [TErr, ClErr]")
            #     except Exception as ex:
            #         logger.exception(ex)
            #         token = new_token
            #         api, _ = get_api(token)
            #         parser = QiwiPaymentsParser(api, on_new_payment)
            #         logger.info(f"Parsing payments with new qiwi {token}")
            #     finally:
            #         await parser.api.close()

            await sleep(self.sleep_time, int)

    def stop(self):
        self._working = False
