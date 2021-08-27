import re
from pyrogram.errors.exceptions.not_acceptable_406 import PhoneNumberInvalid
from aiogram import types
from telethon import TelegramClient, events, sync

from aiogram.dispatcher import FSMContext

from data.states import BtcClient
from loader import dp, client

commands = ["btc_api", "btc_outs", "btc_pays"]


def parse_phone(phone):
    """Parses the given phone, or returns `None` if it's invalid."""
    if isinstance(phone, int):
        return str(phone)
    else:
        phone = re.sub(r"[()\s-]", "", str(phone))
        if phone[1:].isdigit():
            return phone


@dp.message_handler(commands=commands, admins_chat=True, is_admin=True)
async def api_info(message: types.Message):
    if not client.is_connected:
        authed = await client.connect()
    else:
        await client.disconnect()  # get new con info
        authed = await client.connect()
    if not authed:
        await message.answer("Введи тилифон заибал")
        await BtcClient.new_phone.set()
        return

    me = await client.get_me()
    await message.answer(f"Имя: {me.first_name}\nAмилия: @{me.username}")
    await client.disconnect()


@dp.message_handler(state=BtcClient.new_phone, admins_chat=True, is_admin=True)
async def phone_number(message: types.Message, state: FSMContext):
    phone = parse_phone(message.text)
    if phone:
        async with state.proxy() as data:
            data["phone"] = phone
            try:
                code = await client.send_code(phone)
            except PhoneNumberInvalid:
                await message.answer("Неправильный телефон! Ввиди ищо раз сука")
            data["code_hash"] = code.phone_code_hash

        await message.answer("Отправил смс с кодом входа, введи сука!")
        await BtcClient.new_code.set()

    else:
        await message.answer("Неправильный телефон! Ввиди ищо раз сука")


@dp.message_handler(state=BtcClient.new_code, admins_chat=True, is_admin=True)
async def code_request(message: types.Message, state: FSMContext):
    print(message.text)
    async with state.proxy() as data:
        print(data["phone"])
        signed = await client.sign_in(data["phone"], data["code_hash"], message.text)

    if not signed:
        await message.answer("дАВАЙ ДРУГОЙ КОД ЗАИБАЛ")
        return

    await message.answer("Вошел!")
    me = await client.get_me()
    await message.answer(f"Имя: {me.first_name}\nAмилия: @{me.username}")
    await client.disconnect()
    await state.finish()
    print(signed)
