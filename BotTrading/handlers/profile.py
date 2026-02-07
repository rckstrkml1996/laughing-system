from random import randint

from aiogram import types

from loader import config
from models import TradingUser
from data import texts, keyboards


async def portfile(message: types.Message, user: TradingUser):
    await message.answer(texts.zap_text, reply_markup=keyboards.main_keyboard)
    await message.answer_photo(
        "https://telegra.ph/file/d13b29dd860de1ea72125.png",
        texts.profile.format(
            amount=user.balance,
            user_id=user.cid,
            live_count=randint(1451, 1549),
        ),
        reply_markup=keyboards.portfile_keyboard(
            config.tdg_otz_link, config.trading_sup_username
        ),
    )
