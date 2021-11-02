import os
from asyncio import sleep

from aiogram import Bot
from aiogram.utils.emoji import emojize
from aiogram.utils.exceptions import MessageToEditNotFound
from loguru import logger

from customutils.config import BotsConfig
from customutils import datetime_local_now
from models import CasinoUser, TradingUser, EscortUser


class DynamicPinner:
    STANDART_TEXT = emojize("Стандартный закреп, {time} :sparkle:")

    def __init__(self, bot: Bot, config: BotsConfig):
        if not isinstance(bot, Bot):
            raise TypeError(
                f"Argument 'bot' must be an instance of Bot, not '{type(bot).__name__}'"
            )

        if not isinstance(config, BotsConfig):
            raise TypeError(
                f"Argument 'config' must be an instance of BotsConfig, not '{type(config).__name__}'"
            )

        self.bot = bot
        self.config = config

        self._working = False

    def get_pin_text(self):
        if not os.path.exists(self.config.pin_path):
            with open(self.config.pin_path, "w", encoding="utf-8") as f:
                f.write(self.STANDART_TEXT)
                text = self.STANDART_TEXT
        else:
            with open(self.config.pin_path, "r", encoding="utf-8") as f:
                text = f.read()

        return text

    async def pin_message(self, text):
        msg = await self.bot.send_message(self.config.workers_chat, text)
        await self.bot.pin_chat_message(
            self.config.workers_chat, msg.message_id, disable_notification=True
        )
        self.config.pinned_msg_id = msg.message_id
        logger.info(f"Pinned new message with id:{msg.message_id}")

    def get_formatted_pin_text(self, text):
        localnow = datetime_local_now()
        timenow = localnow.strftime("%H:%M, %S cек")

        topd_worker = "Хз"

        in_casino = CasinoUser.select().count()
        in_trading = TradingUser.select().count()
        in_escort = EscortUser.select().count()

        return emojize(
            text.format(
                services_status=self.get_work_status(),
                topd_worker=topd_worker,
                time=timenow,
                in_casino=in_casino,
                in_trading=in_trading,
                in_escort=in_escort,
            )
        )

    async def start(self):
        self._working = True

        while self._working:
            text = self.get_pin_text()
            formatted = self.get_formatted_pin_text(text)

            if self.config.pinned_msg_id is not None:
                try:
                    await self.bot.edit_message_text(
                        formatted, self.config.workers_chat, self.config.pinned_msg_id
                    )
                    logger.debug(
                        f"Edited pinned message id:{self.config.pinned_msg_id}"
                    )
                except MessageToEditNotFound:
                    await self.pin_message(formatted)
                except Exception as ex:
                    logger.error(ex)

            await sleep(self.config.pin_update_time)

        # await self.bot.session.close() # if outside executor

    def stop(self):
        self._working = False

    def get_work_status(self):
        casino_work = self.config.casino_work
        escort_work = self.config.escort_work
        trading_work = self.config.trading_work

        all_work = casino_work and escort_work and trading_work

        return emojize(
            "{casino_status}\n"
            "{escort_status}\n"
            "{trading_status}\n"
            "{team_status}".format(
                casino_status=f":full_moon: Казино СКАМ"
                if casino_work
                else f":new_moon: <del>Казино СКАМ</del>",
                escort_status=f":full_moon: Эскорт СКАМ"
                if escort_work
                else f":new_moon: <del>Эскорт СКАМ</del>",
                trading_status=f":full_moon: Трейдинг СКАМ"
                if trading_work
                else f":new_moon: <del>Трейдинг СКАМ</del>",
                team_status=":full_moon: Общий статус: <b>Ворк</b>"
                if all_work
                else ":new_moon: Общий статус: <b>Не ворк</b>",
            )
        )

    def save_new_pin_text(self, text):
        with open(self.config.pin_path, "w", encoding="utf-8") as f:
            f.write(text)
