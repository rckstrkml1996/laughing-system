from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from loader import dp
from data import texts
from data.states import SetProfitStick
from data.keyboards import *


@dp.callback_query_handler(state="*", text="cancel", admins_chat=True)
async def cancel(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.debug(f"Cancelling state {current_state} in admins chat")
    await state.finish()


@dp.message_handler(state="*", commands=["help", "info"], admins_chat=True)
async def help_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logger.debug(f"Cancelling state {current_state} in admins chat")
        await state.finish()

    await message.answer(texts.admins_help_text)


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


@dp.message_handler(
    commands=["prftstick", "set_profit_sticker"], admins_chat=True, is_admin=True
)
async def sticker_command(message: types.Message):
    await message.answer("Отправь мне любой стикер")
    await SetProfitStick.main.set()


@dp.message_handler(
    state=SetProfitStick.main,
    content_types=["sticker"],
    admins_chat=True,
    is_admin=True,
)
async def set_profit_sticker(message: types.Message, state: FSMContext):
    config.profit_sticker_id = message.sticker.file_id
    await state.finish()
    await message.answer("Сохранил!")


@dp.message_handler(
    state=SetProfitStick.main,
    admins_chat=True,
    is_admin=True,
)
async def close_profit_sticker(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Ну и иди нахуй со своим стиком :(")
