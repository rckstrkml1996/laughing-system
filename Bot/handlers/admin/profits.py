from asyncio import sleep
import re
from time import time

from pyrogram.errors.exceptions.not_acceptable_406 import PhoneNumberInvalid
from aiogram.utils.emoji import emojize
from aiogram import types
from aiogram.dispatcher import FSMContext
from customutils.models import Profit

from loader import dp, client
from config import ServiceNames
from data import payload
from data.states import BtcClient


async def get_wallet_msg():  # shitcode but work
    await sleep(0.3)  # update new msgs
    msgs = await client.get_history("BTC_CHANGE_BOT", limit=1)
    message = msgs[0]
    if message.text.startswith(emojize(":briefcase: Кошелек BTC")):
        return message
    else:
        await sleep(0.1)
        return await get_wallet_msg()


async def get_create_check_msg():
    await sleep(0.3)
    msgs = await client.get_history("BTC_CHANGE_BOT", limit=1)
    message = msgs[0]
    if message.text.startswith(emojize(":dollar: Вы можете создать чек или")):
        return message
    else:
        await sleep(0.1)
        return await get_create_check_msg()


async def get_choice_curr_msg():
    await sleep(0.3)
    msgs = await client.get_history("BTC_CHANGE_BOT", limit=1)
    message = msgs[0]
    if message.text == "Выберите валюту":
        return message
    else:
        await sleep(0.1)
        return await get_choice_curr_msg()


async def get_check_inst():
    await sleep(0.3)
    msgs = await client.get_history("BTC_CHANGE_BOT", limit=3)
    if msgs[0].text == "Ошибка!\n\nНедостаточно средств!":
        return False

    text = msgs[1].text
    if msgs[2].text.startswith(
        "Чтобы другой пользователь смог получить BTC отправьте ему ссылку или QR код"
    ):
        return text
    else:
        await sleep(0.1)
        return await get_check_inst()


async def made_check(amount):
    if isinstance(amount, int):
        amount = str(amount)

    if amount == "0" or not amount.isdigit():
        return False

    if not client.is_connected:
        authed = await client.connect()
    else:
        await client.disconnect()  # get new con info
        authed = await client.connect()
    if not authed:
        return False

    await client.send_message("BTC_CHANGE_BOT", emojize(":briefcase: Кошелек"))
    message = await get_wallet_msg()
    await client.request_callback_answer(
        chat_id=message.chat.id,
        message_id=message.message_id,
        callback_data=message.reply_markup.inline_keyboard[1][0].callback_data,
    )
    message = await get_create_check_msg()
    await client.request_callback_answer(
        chat_id=message.chat.id,
        message_id=message.message_id,
        callback_data=message.reply_markup.inline_keyboard[0][0].callback_data,
    )
    message = await get_choice_curr_msg()
    await client.request_callback_answer(
        chat_id=message.chat.id,
        message_id=message.message_id,
        callback_data=message.reply_markup.inline_keyboard[0][1].callback_data,
    )
    await client.send_message("BTC_CHANGE_BOT", amount)

    check = await get_check_inst()
    return check

    await client.disconnect()


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "truepay", admins_chat=True, is_admin=True
)
async def truepay_qr_command(query: types.CallbackQuery):
    profit_id = query.data.split("_")[1]

    try:
        profit = Profit.get(id=profit_id)
        worker = profit.owner
        if profit.done:
            await query.answer("Уже выплачено!")
            await query.message.delete()
            return

        check = await made_check(profit.share)
        if check:
            profit.done = True
            profit.save()

            await dp.bot.send_message(
                worker.cid, f"Выплата ебать <b>{profit.amount} RUB</b>\n{check}"
            )
            await query.message.edit_text(
                payload.profit_complete_text.format(
                    share=profit.share,
                    profit_link=profit.msg_url,  # save link in base
                    cid=worker.cid,
                    name=worker.username if worker.username else worker.name,
                    service=ServiceNames[profit.service],
                    amount=profit.amount,
                )
            )
        else:
            await query.answer("Похоже не хватает баланса в банкире или что-то!")
    except Profit.DoesNotExist:  # log
        await query.answer("Ошибка в базе!")


def parse_phone(phone):
    """Parses the given phone, or returns `None` if it's invalid."""
    if isinstance(phone, int):
        return str(phone)
    else:
        phone = re.sub(r"[()\s-]", "", str(phone))
        if phone[1:].isdigit():
            return phone


@dp.message_handler(commands=["btc_auth"], admins_chat=True, is_admin=True)
async def api_info(message: types.Message):
    if not client.is_connected:
        authed = await client.connect()
    else:
        await client.disconnect()  # get new con info
        authed = await client.connect()
    if not authed:
        await message.answer("Не авторизован!\nВведи номер телеграмм:")
        await BtcClient.new_phone.set()
        return

    me = await client.get_me()
    await message.answer(f"Авторизован!\nИмя: {me.first_name}\nAмилия: @{me.username}")
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

        await message.answer("Отправил смс с кодом входа, введи код:")
        await BtcClient.new_code.set()

    else:
        await message.answer("Неправильный номер телефона! Введите ещо раз")


@dp.message_handler(state=BtcClient.new_code, admins_chat=True, is_admin=True)
async def code_request(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        signed = await client.sign_in(data["phone"], data["code_hash"], message.text)

    if not signed:
        await message.answer("Не вошел! Неправильный код! Введите новый:")
        return

    me = await client.get_me()
    await message.answer(f"Вошел! Как - \nИмя: {me.first_name}\nAмилия: @{me.username}")
    await client.disconnect()
    await state.finish()
