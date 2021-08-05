import random

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from data import payload
from data.keyboards import summary_start_keyboard, summary_blocked_keyboard
from models import Worker, Payment
from .summary import new_request
from .panel import worker_welcome


@dp.message_handler(commands="start")
async def welcome(message: types.Message):
    try:
        worker = Worker.get(cid=message.chat.id)
        if worker.status == 0:  # если он без статуса
            if worker.send_summary:
                await message.answer(payload.summary_reviewing_text)
            else:
                await new_request(message)
        elif worker.status == 1:  # если воркер заблокан
            await message.answer(payload.summary_blocked_text, reply_markup=summary_blocked_keyboard)
        else:  # если чел уже воркер
            await worker_welcome(message)  # workers menu
    except Worker.DoesNotExist:
        Worker.create(cid=message.chat.id,
                      username=message.chat.username, name=message.chat.full_name)
        await new_request(message)


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "code")
async def code(query: types.CallbackQuery):
    key = query.data.split("_")[1]
    try:
        pay = Payment.get(key=key)
        pay.code = True
        pay.save()
        await query.answer("Сохранено!")
    except Payment.DoesNotExist:
        pass


@dp.message_handler(is_worker=False)
async def new_worker(message: types.Message):
    try:
        worker = Worker.get(cid=message.chat.id)
        if worker.status != 1:  # если не заблокирован
            await message.answer(payload.summary_text, reply_markup=summary_start_keyboard)
    except Worker.DoesNotExist:
        await welcome(message)  # new user to base
