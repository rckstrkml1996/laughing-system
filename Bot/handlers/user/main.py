from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from loader import dp
from utils import basefunctional
from data import payload
from data.keyboards import summary_start_keyboard, summary_blocked_keyboard
from models import Worker
from .summary import new_request
from .panel import worker_welcome


@dp.message_handler(commands="start", state="*")
async def welcome(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logger.debug(f"Cancelling state {current_state} in bot start")
        await state.finish()

    try:
        worker = Worker.get(cid=message.chat.id)
        if worker.status == 0:  # если он без статуса
            logger.debug(
                f"User - {message.chat.id}:{worker.status}, in base but dont send summary"
            )
            if worker.send_summary:
                await message.answer(payload.summary_reviewing_text)
            else:
                await new_request(message)
        elif worker.status == 1:  # если воркер заблокан
            logger.debug(
                f"Blocked Worker - {message.chat.id}:{worker.status}, made /start to bot"
            )
            await message.answer(
                payload.summary_blocked_text, reply_markup=summary_blocked_keyboard
            )
        else:  # если чел уже воркер
            logger.debug(
                f"Worker - {message.chat.id}:{worker.status}, made /start to bot"
            )
            await worker_welcome(message)  # workers menu
    except Worker.DoesNotExist:
        logger.debug(f"User - {message.chat.id}, first time start bot")
        basefunctional.create_worker(
            chat_id=message.chat.id,
            name=message.chat.full_name,
            username=message.chat.username,
        )
        await new_request(message)


@dp.message_handler(is_worker=False)
async def new_worker(message: types.Message):
    try:
        worker = Worker.get(cid=message.chat.id)
        if worker.status != 1:  # если не заблокирован
            await message.answer(
                payload.summary_text, reply_markup=summary_start_keyboard
            )
    except Worker.DoesNotExist:
        await welcome(message, dp.current_state())  # new user to base
