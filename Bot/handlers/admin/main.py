from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from loader import dp
from config import config
from data import payload
from data.keyboards import *


@dp.callback_query_handler(state="*", text="cancel", admins_chat=True)
async def cancel(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.debug(f"Cancelling state {current_state} in admins chat")
    await state.finish()


# WORKING FILE IDS AND CHANGING PHOTOS


@dp.message_handler(content_types=["photo"], admins_chat=True, is_admin=True)
async def photo_hash(message: types.Message):
    if message.caption == "/get_id":
        logger.debug(f"sending photo file id to admin - {message.from_user.id}.")
        await message.answer(message.photo[-1].file_id)


@dp.message_handler(
    commands=["new_design", "new_dsgn"], admins_chat=True, is_admin=True
)
async def new_design_command(message: types.Message):
    logger.debug(f"admin chat /new_desing is stupid {message.from_user.id}")
