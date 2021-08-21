from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from config import config
from data import payload
from data.keyboards import *
from data.states import Pin
from utils.executional import new_pin_text
from utils.pinner import format_pin_text


@dp.message_handler(commands=["pinned", "pin"], admins_type=True)
async def pinned_command(message: types.Message):
    if message.from_user.id not in config("admins_id"):
        return

    await message.answer(payload.pin_text())
    await message.reply(payload.pin_help_text, reply_markup=change_pin_keyboard)


@dp.callback_query_handler(text="change_pin", admins_type=True)
async def change_pin(query: types.CallbackQuery):
    if query.from_user.id not in config("admins_id"):
        await query.answer("Ты не админ)")
        return

    await query.message.answer("Введите новый текст для закрепа:")
    await Pin.change.set()


@dp.message_handler(state=Pin.change, admins_type=True)
async def new_pin(message: types.Message, state: FSMContext):
    await message.answer(message.text, reply_markup=new_pin_keyboard)
    async with state.proxy() as data:
        data['pin'] = message.text
    await Pin.new.set()


@dp.callback_query_handler(state=Pin.new, text="savepin", admins_type=True)
async def save_pin(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pin = data['pin']
        try:
            msg = await query.message.answer(await format_pin_text(pin))
            await msg.reply("Новый закреп.")
            new_pin_text(pin)
        except KeyError as e:
            await query.message.answer(f"Вы ввели неправильное сокращения для динамического закрепа - {{{str(e)[1:-1]}}}")
            await state.finish()
            return

    await query.answer("Сохранено")
    await query.message.delete()
    await state.finish()


@dp.callback_query_handler(state=Pin.new, text="unsavepin", admins_type=True)
async def unsave_pin(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Закреп останется прежним.")
    await state.finish()


@dp.message_handler(state=Pin.new, admins_type=True)
async def unsave_pin(message: types.Message, state: FSMContext):
    await message.answer("Закреп останется прежним.")
    await state.finish()
