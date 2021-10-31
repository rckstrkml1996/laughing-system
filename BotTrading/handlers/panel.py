import re
from random import randint

from aiogram import types
from aiogram.dispatcher import FSMContext
from qiwiapi import QiwiApi, get_api
from qiwiapi.exceptions import InvalidToken, InvalidAccount
from models import TradingUser, TradingPayment

from loader import dp
from data import texts
from data.keyboards import *
from data.states import Withdraw, Deposit


@dp.message_handler(regexp="профил")
async def my_profile(message: types.Message):
    try:
        user = TradingUser.get(cid=message.chat.id)
        await message.answer(
            texts.my_profile_text.format(
                balance=user.balance, cid=user.cid, deals_count=randint(1900, 3000)
            )
        )
    except TradingUser.DoesNotExist:
        pass


@dp.message_handler(regexp="вывест")
async def withdraw(message: types.Message):
    try:
        user = TradingUser.get(cid=message.chat.id)
        await message.answer(texts.withdraw_text.format(balance=user.balance))
        await Withdraw.count.set()
    except TradingUser.DoesNotExist:
        pass


@dp.message_handler(regexp="пополн")
async def my_profile(message: types.Message):
    try:
        user = TradingUser.get(cid=message.chat.id)
        await message.answer(texts.deposit_count_text.format(balance=user.balance))
        await Deposit.count.set()
    except TradingUser.DoesNotExist:
        pass


@dp.message_handler(regexp="счет|счёт")
async def ecn_show(message: types.Message):
    try:
        await message.answer(texts.ecn_show_text, reply_markup=actives_keyboard)
    except TradingUser.DoesNotExist:
        pass


@dp.message_handler(regexp="поддержк")
async def support_show(message: types.Message):
    await message.answer(
        texts.support_text.format(sup_username=config.trading_sup_username)
    )


@dp.message_handler(state=Deposit.count)
async def deposit_entered(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        message.reply(texts.int_error_text)
        return

    try:
        token = config.qiwi_tokens
        if isinstance(token, list):
            token = token[0]
    except NoOptionError:
        config.trading_work = False  # than change as notify
        return

    try:
        user = TradingUser.get(cid=message.chat.id)

        if int(message.text) < config.min_deposit:
            await message.answer(texts.deposit_minerror_text)
        else:
            api, proxy_url = get_api(token)
            try:
                profile = await api.get_profile()
                await api.close()
                account = profile.contractInfo.contractId

                pay = TradingPayment.create(
                    owner=user,
                    comment=f"bnc{randint(111111, 999999)}",
                    amount=message.text,
                )
                await message.answer(
                    texts.deposit_form_text.format(
                        count=pay.amount,
                        qiwi_number=account,
                        comment=pay.comment,
                    ),
                    reply_markup=payment_keyboard(pay.amount, account, pay.comment),
                )
                await state.finish()
            except (InvalidToken, InvalidAccount):  # than change as notify
                pass
    except TradingUser.DoesNotExist:
        pass  # log


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "check", state="*")
async def check_pay(query: types.CallbackQuery):
    try:
        user = TradingUser.get(cid=query.message.chat.id)
        comment = query.data.split("_")[1]
        try:
            payment = TradingPayment.get(owner=user, comment=comment)
            if payment.done:
                payment.delete_instance()
                user.balance += payment.amount  # pay amount changes in bot!
                user.save()
                await query.message.answer(
                    texts.add_succesful.format(amount=payment.amount)
                )
            else:
                await query.message.answer(texts.add_unsuccesful)
        except TradingPayment.DoesNotExist:
            await query.message.answer(
                "Похоже вы уже оплатили этот счёт или он не существует."
            )
    except TradingUser.DoesNotExist:
        pass


@dp.message_handler(state=Withdraw.count)
async def withdraw_entered(message: types.Message, state: FSMContext):
    try:
        user = TradingUser.get(cid=message.chat.id)
        try:
            if int(message.text) < config.min_withdraw:
                await message.answer(texts.withdraw_min_text)
            elif int(message.text) > user.balance:
                await message.reply(
                    texts.withdraw_overprice.format(balance=user.balance)
                )
            else:
                async with state.proxy() as data:
                    data["count"] = message.text.replace(";", " ")
                await message.answer(texts.withdraw_req_text)
                await Withdraw.requisites.set()
        except ValueError:
            await message.reply(texts.int_error_text)
            await state.finish()
    except TradingUser.DoesNotExist:
        pass  # log


@dp.message_handler(state=Withdraw.requisites)
async def requisites_entered(message: types.Message, state: FSMContext):
    try:
        user = TradingUser.get(cid=message.chat.id)
        async with state.proxy() as data:
            user.balance -= int(data["count"])
            user.save()
        await message.reply(texts.withdraw_done_text)
        await state.finish()
    except TradingUser.DoesNotExist:
        pass  # log


@dp.callback_query_handler(state="*", text="back")
async def cancel_handler(query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await query.message.delete()
    await query.message.answer("Отменено")
