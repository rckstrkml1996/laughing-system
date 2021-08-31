from aiogram import types
from customutils.models import Worker

from loader import dp
from config import config
from data import payload
from data.keyboards import *


@dp.message_handler(regexp="эскорт", is_worker=True, state="*")
async def casino_info(message: types.Message):
    worker = Worker.get(cid=message.from_user.id)
    await message.answer(
        payload.escort_text.format(
            worker_id=worker.uniq_key,
        ),
        reply_markup=escort_keyboard,
        disable_web_page_preview=True,
    )
