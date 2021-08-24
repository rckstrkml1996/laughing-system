import random
from configparser import NoOptionError

from aiogram import types
from aiogram.types import ChatType
from aiogram.dispatcher.filters.builtin import Text
from aiogram.utils.markdown import quote_html
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound
from aiogram.utils.emoji import emojize
from loguru import logger

from customutils.qiwiapi import QiwiApi
from customutils.models import CasinoUser, CasinoUserHistory, CasinoPayment
from customutils.qiwiapi.exceptions import InvalidToken, InvalidAccount

from loader import dp
from config import config
from data.states import SelfCabine, AddBalance, OutBalance
from data import payload
import keyboards


PROMOS = {}
FAKE_NUMBER = "666666666"
WORKERS_CHAT = "None"
OUT_CHAT = "None"

"""
Пополнение, вывод - тут
"""


@dp.message_handler(Text(startswith="пополн", ignore_case=True), state="*")
async def add_in_game(message: types.Message):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(payload.add_text)
        await AddBalance.amount.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"#{message.chat.id} - does not exist")


@dp.message_handler(
    lambda mes: not mes.text.isdigit(),
    state=AddBalance.amount,
)
async def add_reqiz_invalid(message: types.Message):
    await message.reply("Сумма должна быть числом.\n\nВведите сумму пополнения")


@dp.message_handler(state=AddBalance.amount)
async def add_reqiz(message: types.Message, state: FSMContext):
    min_depos = config("min_deposit")
    amount = int(message.text)
    if amount < min_depos:
        await message.answer(f"Минимальная сумма депозита - <b>{min_depos} RUB</b>")
        return
    try:
        user = CasinoUser.get(cid=message.chat.id)
        async with state.proxy() as data:
            data["amount"] = amount
        comment = random.randint(1000000, 9999999)

        try:
            token = config("qiwi_tokens")
            if isinstance(token, list):
                token = token[0]
        except NoOptionError:
            config.edit_config("casino_work", False)  # than change as notify
            return

        api = QiwiApi(token)

        try:
            profile = await api.get_profile()
            account = profile.contractInfo.contractId
            await message.answer(
                payload.add_req_text(amount, comment, account),
                reply_markup=keyboards.add_req_keyboard(amount, comment, account),
            )
            CasinoPayment.create(owner=user, comment=comment, amount=amount)
        except (InvalidToken, InvalidAccount):  # than change as notify
            pass

    except CasinoUser.DoesNotExist:
        logger.debug(f"#{message.chat.id} - does not exist")
    finally:
        await SelfCabine.main.set()


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "check", state="*")
async def add_check(query: types.CallbackQuery):
    try:
        user = CasinoUser.get(cid=query.message.chat.id)
        comment = query.data.split("_")[1]

        try:
            payment = CasinoPayment.get(owner=user, comment=comment)
            if payment.done:
                user.balance += payment.amount + user.bonus
                user.save()
                await query.message.answer(
                    payload.add_succesful(payment.amount + user.bonus)
                )
        except CasinoPayment.DoesNotExist:
            logger.warning(f"for #{query.from_user.id} - payment does not exist")
            await query.message.answer(
                "Похоже вы уже оплатили этот счёт или он не существует."
            )
    except CasinoUser.DoesNotExist:
        logger.debug(f"#{query.message.chat.id} - does not exist")


@dp.message_handler(Text(startswith="выв", ignore_case=True), state="*")
async def out_game(message: types.Message):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(
            emojize(
                f"Введите сумму вывода :money_with_wings: \
			\nВаш баланс: <b>{user.balance} RUB</b>"
            ),
            reply_markup=keyboards.cancel_keyboard,
        )
        await OutBalance.amount.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"#{message.chat.id} - does not exist")


@dp.message_handler(
    lambda mes: not mes.text.isdigit() or mes.text == "0",
    state=OutBalance.amount,
)
async def out_amount_invalid(message: types.Message):
    await message.reply(quote_html("Вы ввели некорректную сумму вывода!"))


@dp.message_handler(state=OutBalance.amount)
async def out_amount(message: types.Message, state: FSMContext):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        if user.balance >= int(message.text):
            async with state.proxy() as data:
                data["amount"] = int(message.text)
            await message.answer(payload.out_req_text)
            await OutBalance.number.set()
        elif user.balance < int(message.text):
            await message.answer(
                "Недостаточно средств для вывода",
                reply_markup=keyboards.cancel_keyboard,
            )
    except CasinoUser.DoesNotExist:
        logger.debug(f"#{message.chat.id} - does not exist")


@dp.message_handler(regexp="\+\d{10,}|\d{10,}", state=OutBalance.number)
async def out_number(message: types.Message, state: FSMContext, regexp):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        group = regexp.group()
        if group[0] == "+":
            group = group[1:]

        lmbd = lambda b: b.replace("r", "").replace("u", "")
        fake_nums = list(map(lmbd, config("fake_numbers"))) + list(
            map(lmbd, config("fake_cards"))
        )

        if group in fake_nums:
            async with state.proxy() as data:
                user.balance -= data["amount"]
                if user.balance < 0:
                    await message.answer("Ошибка!")
                    return
                user.save()
                CasinoUserHistory.create(
                    owner=user,
                    amount=data["amount"],
                    editor=1,
                    balance=user.balance,
                )

            await message.answer(
                f"Баланс: <b>{user.balance} RUB</b>\n" + payload.out_req_succesful,
                reply_markup=keyboards.main_keyboard(),
            )
            await state.finish()
        else:
            await message.answer(
                payload.out_invreq_text, reply_markup=keyboards.main_keyboard()
            )
            await state.finish()
    except CasinoUser.DoesNotExist:
        logger.debug(f"#{message.chat.id} - does not exist")


@dp.message_handler(state=OutBalance.number)
async def invalid_outnumber(message: types.Message, state: FSMContext):
    await message.answer("Введите корректный номер.")


@dp.message_handler(Text(contains="промо", ignore_case=True), state="*")
async def insert_promo(message: types.Message):
    await message.answer("Введите промокод", reply_markup=keyboards.cancel_keyboard)
    await OutBalance.promo.set()


@dp.message_handler(state=OutBalance.promo)
async def promo_complete(message: types.Message):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        if message.text in PROMOS:
            amount = PROMOS[message.text]
            if user.bonus == amount:
                await message.answer(
                    "Такой промокод уже активирован",
                    reply_markup=keyboards.selfcab_keyboard,
                )
                return
            user.bonus = amount
            user.save()
            await message.answer(
                f"Промокод на {amount} RUB активирован!",
                reply_markup=keyboards.selfcab_keyboard,
            )
        else:
            await message.answer(
                "Такой промокод не удалось найти",
                reply_markup=keyboards.selfcab_keyboard,
            )
    except CasinoUser.DoesNotExist:
        logger.info(f"CasinoUser {message.chat.id} does not exist")
    finally:
        await SelfCabine.main.set()
