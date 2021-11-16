from asyncio import sleep
import re

from pyrogram.errors.exceptions.not_acceptable_406 import PhoneNumberInvalid
from aiogram.utils.emoji import emojize
from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from loader import dp, banker_client, BTC_REGEX
from models import Profit
from data import texts
from data.keyboards import *
from data.states import BtcClient
from data.texts import (
    btc_authed_text,
    check_true_text,
)


@dp.message_handler(regexp=BTC_REGEX, admins_chat=True)
async def new_btc_check(message: types.Message, regexp):
    if not banker_client.is_connected:
        authed = await banker_client.connect()
    else:
        await banker_client.disconnect()  # get new con info
        authed = await banker_client.connect()
    if not authed:
        await message.answer("Не авторизован!\nВведи номер телеграмм:")
        await BtcClient.new_phone.set()
        return
    check = regexp.group(1)
    await banker_client.send_message("BTC_CHANGE_BOT", f"/start {check}")
    await message.answer(check_true_text.format(amount=100))


async def get_wallet_msg():  # shitcode but work
    await sleep(0.3)  # update new msgs
    msgs = await banker_client.get_history("BTC_CHANGE_BOT", limit=1)
    message = msgs[0]
    if message.text.startswith(emojize(":briefcase: Кошелек BTC")):
        return message
    else:
        await sleep(0.1)
        return await get_wallet_msg()


async def get_create_check_msg():
    await sleep(0.3)
    msgs = await banker_client.get_history("BTC_CHANGE_BOT", limit=1)
    message = msgs[0]
    if message.text.startswith(emojize(":dollar: Вы можете создать чек или")):
        return message
    else:
        await sleep(0.1)
        return await get_create_check_msg()


async def get_choice_curr_msg():
    await sleep(0.3)
    msgs = await banker_client.get_history("BTC_CHANGE_BOT", limit=1)
    message = msgs[0]
    if message.text == "Выберите валюту":
        return message
    else:
        await sleep(0.1)
        return await get_choice_curr_msg()


async def get_check_inst():
    await sleep(0.3)
    msgs = await banker_client.get_history("BTC_CHANGE_BOT", limit=3)
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
    if not banker_client.is_connected:
        authed = await banker_client.connect()
    else:
        await banker_client.disconnect()  # get new con info
        authed = await banker_client.connect()
    if not authed:
        return False
    await banker_client.send_message("BTC_CHANGE_BOT", emojize(":briefcase: Кошелек"))
    message = await get_wallet_msg()
    await banker_client.request_callback_answer(
        chat_id=message.chat.id,
        message_id=message.message_id,
        callback_data=message.reply_markup.inline_keyboard[1][0].callback_data,
    )
    message = await get_create_check_msg()
    await banker_client.request_callback_answer(
        chat_id=message.chat.id,
        message_id=message.message_id,
        callback_data=message.reply_markup.inline_keyboard[0][0].callback_data,
    )
    message = await get_choice_curr_msg()
    await banker_client.request_callback_answer(
        chat_id=message.chat.id,
        message_id=message.message_id,
        callback_data=message.reply_markup.inline_keyboard[0][1].callback_data,
    )
    await banker_client.send_message("BTC_CHANGE_BOT", amount)
    check = await get_check_inst()
    await banker_client.disconnect()
    return check


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "truepay",
    admins_chat=True,
    is_admin=True,
    state="*",
)
async def truepay_qr_command(query: types.CallbackQuery):
    profit_id = query.data.split("_")[1]
    try:
        profit = Profit.get(id=profit_id)
        worker = profit.owner
        if profit.done:
            await query.answer("Уже выплачено, зови кодера!")
            logger.error("Payment already done.")
            return
        check = await made_check(profit.share)
        if check:
            logger.info(f"Payment done: {check}, {profit.done}")
            profit.done = True
            profit.save()
            await dp.bot.send_message(
                worker.cid,
                texts.profit_check_text.format(
                    amount=profit.amount, share=profit.share, check=check
                ),
            )
            await query.message.edit_text(
                texts.admins_profit_complete_text.format(
                    profit_link=profit.msg_url,  # save link in base
                    mention=texts.mention_text.format(
                        user_id=worker.cid,
                        text=worker.name,
                    ),
                    amount=profit.amount,
                    service=profit.service_name,
                    share=profit.share,
                    moll=int(profit.share * 100 / profit.amount),
                    # created_date ..
                    # payed_date ..
                ),
                disable_web_page_preview=True,
            )
        else:
            await query.answer("Похоже не хватает баланса в банкире или что-то!")
            logger.debug("Not enough balance for payment.")
    except Profit.DoesNotExist:  # log
        await query.answer("Ошибка в базе!")
        logger.debug("DB payment error.")


def parse_phone(phone):
    """Parses the given phone, or returns `None` if it's invalid."""
    if isinstance(phone, int):
        return str(phone)
    else:
        phone = re.sub(r"[()\s-]", "", str(phone))
        if phone[1:].isdigit():
            return phone


@dp.message_handler(commands=["btc_auth"], state="*", admins_chat=True, is_admin=True)
async def api_info(message: types.Message):
    if not banker_client.is_connected:
        authed = await banker_client.connect()
    else:
        await banker_client.disconnect()  # get new con info
        authed = await banker_client.connect()
    if not authed:
        await message.answer("Не авторизован!\nВведи номер телеграмм:")
        await BtcClient.new_phone.set()
        return
    me = await banker_client.get_me()
    await message.answer(
        btc_authed_text.format(name=me.first_name, username=me.username)
    )
    logger.debug("BTC authorization completed.")
    await banker_client.disconnect()


@dp.message_handler(state=BtcClient.new_phone, admins_chat=True, is_admin=True)
async def phone_number(message: types.Message, state: FSMContext):
    phone = parse_phone(message.text)
    if phone:
        async with state.proxy() as data:
            data["phone"] = phone
            try:
                code = await banker_client.send_code(phone)
            except PhoneNumberInvalid:
                await message.answer("Неправильный телефон! Ввиди ищо раз сука")
                logger.debug("Phone number is wrong.")
            data["code_hash"] = code.phone_code_hash
        await message.answer("Отправил смс с кодом входа, введи код:")
        logger.debug("SMS sent.")
        await BtcClient.new_code.set()
    else:
        await message.answer("Неправильный номер телефона! Введите ещо раз")
        logger.debug("Phone number is wrong.")


@dp.message_handler(state=BtcClient.new_code, admins_chat=True, is_admin=True)
async def code_request(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        signed = await banker_client.sign_in(
            data["phone"], data["code_hash"], message.text
        )
    if not signed:
        await message.answer("Не вошел! Неправильный код! Введите новый:")
        logger.debug("SMS code is wrong.")
        return
    me = await banker_client.get_me()
    await message.answer(f"Вошел! Как - \nИмя: {me.first_name}\nAмилия: @{me.username}")
    logger.debug("Logged in done.")
    await banker_client.disconnect()
    await state.finish()
