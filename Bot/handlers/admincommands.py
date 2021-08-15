from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from loader import dp
from data import payload
from data.states import Pin
from data.keyboards import *
from utils.pinner import format_pin_text
from utils.executional import get_work_status, new_pin_text
from config import config


@dp.message_handler(commands="work", admins_type=True)
async def work_command(message: types.Message):
    casino_work = config("casino_work")
    escort_work = config("escort_work")
    antikino_work = config("antikino_work")

    all_work = casino_work and escort_work and antikino_work

    await message.answer(
        payload.adm_work_command.format(
            services_status=get_work_status(),
        ),
        reply_markup=admworkstatus_keyboard(all_work)
    )


@dp.callback_query_handler(text="toggleworkstatus", admins_type=True)
async def toggle_work_status(query: types.CallbackQuery):
    if query.from_user.id not in config("admins_id"):
        await query.answer("Ты не админ!")
        return

    casino_work = not config("casino_work")  # return bool values
    escort_work = not config("escort_work")
    antikino_work = not config("antikino_work")

    config.edit_config("casino_work", casino_work)
    config.edit_config("escort_work", escort_work)
    config.edit_config("antikino_work", antikino_work)

    all_work = casino_work and escort_work and antikino_work

    text = payload.adm_work_command.format(
        services_status=get_work_status()
    )

    try:
        await query.message.edit_text(
            text, reply_markup=admworkstatus_keyboard(all_work)
        )
    except MessageNotModified:
        pass
    await dp.bot.send_message(config("workers_chat"), payload.setwork_text if all_work else payload.setdontwork_text)


""" WORKING FILE IDS AND CHANGING PHOTOS """


@dp.message_handler(content_types=["photo"], admins_type=True)
async def photo_hash(message: types.Message):
    if message.from_user.id not in config("admins_id"):
        return

    if message.caption == "/get_id":
        await message.answer(message.photo[-1].file_id)


@dp.message_handler(commands="new_design", admins_type=True)
async def new_design_command(message: types.Message):
    if message.from_user.id not in config("admins_id"):
        return


@dp.message_handler(commands="pinned", admins_type=True)
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
