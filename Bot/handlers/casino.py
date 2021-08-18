from aiogram import types

from config import config
from loader import dp
from data import payload
from data.keyboards import *


@dp.message_handler(regexp="казин")
async def casino_info(message: types.Message):
    await message.answer(
        payload.casino_text.format(
            worker_id=101,
            pay_cards="\n".join(
                map(
                    lambda c: f'&#127479;&#127482; {c[1:]}' if c[0] == "r" else f'&#127482;&#127462; {c[1:]}', config(
                        "fake_cards")
                )
            ),
            pay_qiwis="\n".join(
                map(
                    lambda c: f'&#127479;&#127482; {c[1:]}' if c[0] == "r" else f'&#127482;&#127462; {c[1:]}', config(
                        "fake_numbers")
                )
            ),
        ),
        reply_markup=casino_keyboard,
        disable_web_page_preview=True
    )
