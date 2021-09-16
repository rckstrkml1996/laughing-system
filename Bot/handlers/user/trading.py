import re
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from loguru import logger
from customutils.datefunc import datetime_local_now
from customutils.models import TradingUser, TradingPayment, Worker

from loader import dp, trading_bot
from config import config, html_style_url
from data import payload
from data.keyboards import *

# from data.states import Trading


@dp.message_handler(regexp="трейдин", is_worker=True, state="*")
async def casino_info(message: types.Message):
    worker = Worker.get(cid=message.from_user.id)
    await message.answer(
        payload.trading_text.format(
            worker_id=worker.uniq_key,
            pay_cards="\n".join(
                map(
                    lambda c: f"&#127479;&#127482; {c[1:]}"
                    if c[0] == "r"
                    else f"&#127482;&#127462; {c[1:]}",
                    config("fake_cards"),
                )
            ),
            pay_qiwis="\n".join(
                map(
                    lambda c: f"&#127479;&#127482; {c[1:]}"
                    if c[0] == "r"
                    else f"&#127482;&#127462; {c[1:]}",
                    config("fake_numbers"),
                )
            ),
        ),
        reply_markup=trading_keyboard,
        disable_web_page_preview=True,
    )
