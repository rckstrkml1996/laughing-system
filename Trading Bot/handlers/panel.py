from aiogram import types
import loguru
from peewee import DoesNotExist

from loader import dp
from data import payload
from aiogram.dispatcher import FSMContext
from data.keyboards import *
from customutils.models import Worker
from random import randint
from data.states import Withdraw, Deposit
from data.config import MIN_WITHDRAW, MIN_DEPOSIT


@dp.message_handler(regexp="профил")
async def my_profile(message: types.Message):
    try:
        worker = Worker.get(cid=message.chat.id)
        await message.answer(payload.my_profile_text.format(
                balance=worker.ref_balance, # NOT REF BALANCE
                cid=worker.cid,
                deals_count=randint(700, 3000)
            )
        )
    except Worker.DoesNotExist:
        pass


@dp.message_handler(regexp="вывест")
async def my_profile(message: types.Message):
    try:
        worker = Worker.get(cid=message.chat.id)
        await message.answer(payload.withdraw_text.format(
                balance=worker.ref_balance # NOT REF BALANCE
            )
        )
        await Withdraw.count.set()
    except Worker.DoesNotExist:
        pass

@dp.message_handler(regexp="пополн")
async def my_profile(message: types.Message):
    try:
        await message.answer(payload.deposit_start_text)
        await Deposit.count.set()
    except Worker.DoesNotExist:
        pass

@dp.message_handler(state=Deposit.count)
async def deposit_entered(message: types.Message, state: FSMContext):
    try:
        worker = Worker.get(cid=message.chat.id)
        try:
            if int(message.text) < MIN_DEPOSIT:  # NOT REF BALANCE BUT BALANCE.
                await message.answer(payload.deposit_minerror_text)
            else:
                loguru.logger.info("PAYMENT PROCESSING")
                await state.finish()
        except ValueError:
            await message.reply(payload.int_error_text)
    except Worker.DoesNotExist:
        pass

@dp.message_handler(state=Withdraw.count)
async def withdraw_entered(message: types.Message, state: FSMContext):
    try:
        worker = Worker.get(cid=message.chat.id)
        try:
            if int(message.text) < MIN_WITHDRAW:  # NOT REF BALANCE BUT BALANCE.
                await message.answer(payload.withdraw_min_text)
            elif int(message.text) > worker.ref_balance:
                await message.reply(payload.withdraw_overprice.format(
                    balance=worker.ref_balance
                ))
            else:
                async with state.proxy() as data:
                    data["count"] = message.text.replace(";", " ")
                Withdraw.requisites.set()
        except ValueError:
            await message.reply(payload.int_error_text)
    except Worker.DoesNotExist:
        pass

@dp.message_handler(state=Withdraw.requisites)
async def requisites_entered(message: types.Message, state: FSMContext):
    try:
        worker = Worker(cid=message.chat.id)
        async with state.proxy() as data:
            worker.ref_balance -= int(data["count"])
        await message.reply(payload.withdraw_done_text)
    except Worker.DoesNotExist:
        pass
