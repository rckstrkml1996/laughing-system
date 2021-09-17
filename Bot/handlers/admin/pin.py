from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.text_decorations import html_decoration

from loguru import logger

from loader import dp
from data import payload
from data.keyboards import *
from data.states import Pin
from utils.executional import new_pin_text
from utils.pinner import format_pin_text


@dp.message_handler(
    commands=["pinned", "pin"], admins_chat=True, is_admin=True, state="*"
)
async def pinned_command(message: types.Message):
    text = html_decoration.unparse(payload.pin_text())
    await message.answer(text)
    await message.reply(payload.pin_help_text, reply_markup=change_pin_keyboard)


@dp.callback_query_handler(text="change_pin", admins_chat=True, is_admin=True)
async def change_pin(query: types.CallbackQuery):
    await query.message.answer("Введите новый текст для закрепа:")
    await Pin.change.set()


@dp.message_handler(state=Pin.change, admins_chat=True)
async def new_pin(message: types.Message, state: FSMContext):
    await message.answer(message.text, reply_markup=new_pin_keyboard)
    async with state.proxy() as data:
        data["pin"] = message.text
    await Pin.new.set()


@dp.callback_query_handler(state=Pin.new, text="savepin", admins_chat=True)
async def save_pin(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pin = data["pin"]
        try:
            msg = await query.message.answer(await format_pin_text(pin))
            await msg.reply("Новый закреп.")
            new_pin_text(pin)
        except KeyError as e:
            await query.message.answer(
                f"Вы ввели неправильное сокращения для динамического закрепа - {{{str(e)[1:-1]}}}"
            )
            await state.finish()
            return
    logger.debug("New pin set.")
    await query.answer("Сохранено")
    await query.message.delete()
    await state.finish()


@dp.callback_query_handler(state=Pin.new, text="unsavepin", admins_chat=True)
async def unsave_pin(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Закреп останется прежним.")
    await state.finish()


@dp.message_handler(state=Pin.new, admins_chat=True)
async def unsave_pin(message: types.Message, state: FSMContext):
    await message.answer("Закреп останется прежним.")
    await state.finish()
