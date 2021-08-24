from aiogram import types

from loader import dp
from data.keyboards import main_keyboard, rules_keyboard
from data import payload
from customutils.models import TradingUser
from random import randint

@dp.message_handler(commands="start")
async def welcome(message: types.Message):
    try:
        user = TradingUser.get(cid=message.chat.id)
        await message.answer(payload.my_profile_text.format(
            balance=user.balance,
            cid=user.cid,
            deals_count=randint(1900,3000)
        ), reply_markup=main_keyboard)
    except TradingUser.DoesNotExist:
        await message.answer(payload.welcome_text(message.from_user.full_name), 
                        reply_markup=rules_keyboard)

@dp.message_handler(content_types=["photo"])
async def get_photo(message: types.Message):
    file_id = message.photo[-1].file_id
    print(file_id) # этот идентификатор нужно где-то сохранить
    await message.answer_photo(file_id)