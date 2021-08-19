from aiogram import types

from loader import dp
from data.keyboards import main_keyboard, rules_keyboard
from data import payload

@dp.message_handler(commands="start")
async def welcome(message: types.Message):
    await message.answer(payload.welcome_text.format(
                                username=message.chat.username), 
                        reply_markup=rules_keyboard)

