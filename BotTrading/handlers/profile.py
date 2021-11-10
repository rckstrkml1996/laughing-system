from re import I
from random import randint

from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, config
from models import TradingUser
from data import texts, keyboards


@dp.message_handler(
    Text(startswith="портфель", ignore_case=True), is_user=True, state="*"
)
@dp.message_handler(commands=["start"], is_user=True, state="*")
async def profile(message: types.Message, user: TradingUser):
    await message.answer(texts.zap_text, reply_markup=keyboards.main_keyboard)
    await message.answer(
        texts.profile.format(
            amount=user.balance,
            user_id=user.id,
            live_count=randint(1451, 1549),
        ),
        reply_markup=keyboards.portfile_keyboard(config.trading_sup_username),
    )
