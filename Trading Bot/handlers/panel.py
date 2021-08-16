from aiogram import types
from aiogram.utils.emoji import emojize
import loguru
from peewee import DoesNotExist

from loader import dp
from data import payload
from aiogram.dispatcher import FSMContext
from data.keyboards import *
from customutils.models.models import Worker
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
        if message.text < MIN_DEPOSIT:  # NOT REF BALANCE BUT BALANCE.
            await message.answer(payload.withdraw_min_text)
        else:
            loguru.logger.info("PAYMENT PROCESSING")
    except Worker.DoesNotExist:
        pass
    await state.finish()

@dp.message_handler(lambda mes: not mes.text.isdigit(),
                    state=Deposit.count)
async def deposit_invalid(message: types.Message):
    await message.reply(payload.deposit_minerror_text)

@dp.message_handler(state=Withdraw.count)
async def withdraw_entered(message: types.Message, state: FSMContext):
    try:
        worker = Worker.get(cid=message.chat.id)
        if message.text < MIN_WITHDRAW:  # NOT REF BALANCE BUT BALANCE.
            await message.answer(payload.withdraw_min_text)
        else:
            worker.ref_balance -= int(message.text)
            worker.save()
            await message.answer(payload.withdraw_done_text)
    except Worker.DoesNotExist:
        pass
    await state.finish()

@dp.message_handler(lambda mes: not mes.text.isdigit(),
                    state=Withdraw.count)
async def withdraw_invalid(message: types.Message):
    await message.reply(payload.withdraw_error_text)
