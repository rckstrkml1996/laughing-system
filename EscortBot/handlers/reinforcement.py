from aiogram import types
from aiogram.utils.markdown import quote_html
from aiogram.utils.emoji import emojize
from loguru import logger

import keyboards
from data import payload
from data.config import SHARE, OUT_CHAT, WORKERS_CHAT
from loader import dp
from customutils.models import EscortUser, EscortPayment
from customutils.qiwiapi import QiwiApi


@dp.message_handler(regexp="бал")
async def balance(message: types.Message):
    try:
        user = EscortUser.get(cid=message.chat.id)
        await message.answer(emojize(f":dollar: Ваш баланс: <b>{user.balance} RUB</b>"),
                             reply_markup=keyboards.balance_keyboard)
    except EscortUser.DoesNotExist:
        logger.info("balance func with no base def")


@dp.message_handler(regexp="пополн")
async def add(message: types.Message):
    await message.delete()
    # number = random.choice(list(qiwis.keys())) 	FIXIT: - Enter qiwi's numbers
    pay = EscortPayment.create(cid=message.chat.id)
    await message.answer(payload.add_req_text('number', pay.id),
                         reply_markup=keyboards.add_req_keyboard('number', pay.id))

# bomba coders

@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "check")
async def add_check(query: types.CallbackQuery):
    try:
        user = EscortUser.get(cid=query.message.chat.id)
        comment = query.data.split("_")[1]
        try:
            payment = EscortPayment.get(owner=user, comment=comment)
            if payment.done:
                user.balance += payment.amount + user.bonus
                user.save()
                await query.message.answer(
                    payload.add_succesful(payment.amount + user.bonus)
                )
        except EscortPayment.DoesNotExist:
            logger.warning(f"for #{query.from_user.id} - payment does not exist")
            await query.message.answer(
                "Похоже вы уже оплатили этот счёт или он не существует."
            )
    except EscortUser.DoesNotExist:
        logger.debug(f"#{query.message.chat.id} - does not exist")