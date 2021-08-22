from aiogram import types
from peewee import DoesNotExist
from loader import dp
from data import payload
from aiogram.dispatcher import FSMContext
from data.keyboards import *
from customutils.models import TradingUser
from random import randint
from data.states import Withdraw, Deposit
from data.config import config


@dp.message_handler(regexp="профил")
async def my_profile(message: types.Message):
    try:
        user = TradingUser.get(cid=message.chat.id)
        await message.answer(payload.my_profile_text.format(
            balance=user.balance,  # NOT REF BALANCE
            cid=user.cid,
            deals_count=randint(700, 3000)
            )
        )
    except TradingUser.DoesNotExist:
        pass

@dp.callback_query_handler(text="rules_agreed")
async def rules_agreed(query: types.CallbackQuery):
    await query.message.edit_text(payload.welcome_text(query.from_user.full_name, True))
    TradingUser.create(cid=query.message.chat.id, username=query.from_user.username,
                          fullname=query.from_user.full_name)
    try:
        user = TradingUser.get(cid=query.message.chat.id)
        await query.message.answer(payload.my_profile_text.format(
                                    balance=user.balance,
                                    cid=user.cid,
                                    deals_count=randint(700, 3000)
        ), reply_markup=main_keyboard)
    except TradingUser.DoesNotExist:
        pass

@dp.message_handler(regexp="вывест")
async def withdraw(message: types.Message):
    try:
        user = TradingUser.get(cid=message.chat.id)
        await message.answer(payload.withdraw_text.format(
            balance=user.balance  # NOT REF BALANCE
            )
        )
        await Withdraw.count.set()
    except TradingUser.DoesNotExist:
        pass

@dp.message_handler(regexp="пополн")
async def my_profile(message: types.Message):
    try:
        user = TradingUser.get(cid=message.chat.id)
        await message.answer(payload.deposit_count_text.format(
            balance=user.balance
        ))
        await Deposit.count.set()
    except TradingUser.DoesNotExist:
        pass

@dp.message_handler(regexp="счет|счёт")
async def ecn_show(message: types.Message):
    try:
        await message.answer(payload.ecn_show_text,
                             reply_markup=actives_keyboard)
    except TradingUser.DoesNotExist:
        pass

@dp.message_handler(regexp="поддержк")
async def support_show(message: types.Message):
    await message.answer(payload.support_text)

@dp.message_handler(state=Deposit.count)
async def deposit_entered(message: types.Message, state: FSMContext):
    try:
        user = TradingUser.get(cid=message.chat.id)
        try:
            # NOT REF BALANCE BUT BALANCE.
            if int(message.text) < config("min_deposit"):
                await message.answer(payload.deposit_minerror_text)
            else:
                await message.answer(payload.deposit_form_text.format(
                    count=int(message.text),
                    qiwi_number=13131313, # QIWI NUMBER
                    comment=133131        # GENERATE COMMENT???
                ), reply_markup=payment_keyboard)
                await state.finish()
        except ValueError:
            await message.reply(payload.int_error_text)
            await state.finish()
    except TradingUser.DoesNotExist:
        pass

@dp.message_handler(state=Withdraw.count)
async def withdraw_entered(message: types.Message, state: FSMContext):
    try:
        user = TradingUser.get(cid=message.chat.id)
        try:
            # NOT REF BALANCE BUT BALANCE.
            if int(message.text) < config("min_withdraw"):
                await message.answer(payload.withdraw_min_text)
            elif int(message.text) > user.balance:
                await message.reply(payload.withdraw_overprice.format(
                    balance=user.balance
                ))
            else:
                async with state.proxy() as data:
                    data["count"] = message.text.replace(";", " ")
                await message.answer(payload.withdraw_req_text)
                await Withdraw.requisites.set()
        except ValueError:
            await message.reply(payload.int_error_text)
            await state.finish()
    except TradingUser.DoesNotExist:
        pass

@dp.message_handler(state=Withdraw.requisites)
async def requisites_entered(message: types.Message, state: FSMContext):
    try:
        user = TradingUser.get(cid=message.chat.id)
        async with state.proxy() as data:
            user.balance -= int(data["count"])
            user.save()
        await message.reply(payload.withdraw_done_text)
        await state.finish()
    except TradingUser.DoesNotExist:
        pass
