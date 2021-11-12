from random import randint

from aiogram import types

from loader import config
from models import TradingUser
from data import texts, keyboards


async def portfile(message: types.Message, user: TradingUser):
    await message.answer(texts.zap_text, reply_markup=keyboards.main_keyboard)
    await message.answer(
        texts.profile.format(
            amount=user.balance,
            user_id=user.id,
            live_count=randint(1451, 1549),
        ),
        reply_markup=keyboards.portfile_keyboard(config.trading_sup_username),
    )
