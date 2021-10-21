from aiogram import types

from customutils.models import Worker

from loader import dp
from config import config
from data.payload import trading_text
from data.keyboards import trading_keyboard


@dp.message_handler(regexp="трейдин", is_worker=True, state="*")
async def casino_info(message: types.Message, worker: Worker):
    await message.answer(
        trading_text.format(
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
