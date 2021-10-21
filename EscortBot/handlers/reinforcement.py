import re
from random import randint


from aiogram import types
from aiogram.utils.emoji import emojize
from loguru import logger
from customutils.qiwiapi import QiwiApi
from customutils.qiwiapi.exceptions import InvalidToken, InvalidAccount
from customutils.models import EscortUser, EscortPayment

import keyboards
from config import config
from data import payload
from loader import dp


def get_api(conf_token: str):
    srch = re.search(r"\(([^\(^\)]+)\)", conf_token)
    if srch:
        return QiwiApi(
            token=conf_token.replace(srch.group(0), ""), proxy_url=srch.group(1)
        )
    return QiwiApi(conf_token)


@dp.message_handler(regexp="бал")
async def balance(message: types.Message):
    try:
        user = EscortUser.get(cid=message.chat.id)
        await message.answer(
            emojize(f":dollar: Ваш баланс: <b>{user.balance} RUB</b>"),
            reply_markup=keyboards.balance_keyboard,
        )
        logger.debug(f"{message.chat.id} - checked balance")
    except EscortUser.DoesNotExist:
        logger.info("balance func with no base def")


@dp.message_handler(regexp="пополн")
async def add(message: types.Message):
    try:
        token = config("qiwi_tokens")
        if isinstance(token, list):
            token = token[0]
    except NoOptionError:
        config.edit("escort_work", False)  # than change as notify
        return

    api = get_api(token)
    try:
        profile = await api.get_profile()
        await api.close()
        account = profile.contractInfo.contractId

        user = EscortUser.get(cid=message.chat.id)
        await message.delete()
        pay = EscortPayment.create(owner=user, comment=f"e{randint(11111, 99999)}")
        await message.answer(
            payload.add_req_text(account, pay.comment),
            reply_markup=keyboards.add_req_keyboard(account, pay.comment),
        )
    except (InvalidToken, InvalidAccount):  # than change as notify
        logger.warning(f"{message.chat.id} - invalid account or token")
        pass
    except EscortUser.DoesNotExist:
        logger.debug(f"{message.chat.id} - doesn't exist")


# bomba coders


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "check")
async def add_check(query: types.CallbackQuery):
    try:
        user = EscortUser.get(cid=query.message.chat.id)
        comment = query.data.split("_")[1]
        try:
            payment = EscortPayment.get(owner=user, comment=comment)
            if payment.done:
                payment.delete_instance()
                user.balance += payment.amount  # pay amount changes in bot!
                user.save()
                await query.message.answer(payload.add_succesful(payment.amount))
            else:
                await query.message.answer(payload.add_unsuccesful)
        except EscortPayment.DoesNotExist:
            logger.warning(f"for #{query.from_user.id} - payment does not exist")
            await query.message.answer(
                "Похоже вы уже оплатили этот счёт или он не существует."
            )
    except EscortUser.DoesNotExist:
        logger.debug(f"#{query.message.chat.id} - does not exist")
