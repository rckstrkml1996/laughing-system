from aiogram import types
from aiogram.utils.emoji import emojize

from loader import dp
from data import payload
from data.keyboards import *
from random import randint
from data.states import Withdraw

@dp.message_handler(regexp="профил")
async def my_profile(message: types.Message):
    await message.answer(payload.my_profile_text.format(
            balance=0,
            cid=message.chat.id,
            deals_count=randint(700, 2000)
        )
    )

@dp.message_handler(regexp="вывест")
async def my_profile(message: types.Message):
    await message.answer(payload.withdraw_text.format(
            balance=0
        )
    )
    Withdraw.count.set()