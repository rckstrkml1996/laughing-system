from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from loader import dp, config, status_names
from utils import basefunctional
from data import texts
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
                f"[{message.chat.id}:{worker.status}], in base but dont send summary"
            )
            if worker.send_summary:
                await message.answer(texts.summary_reviewing_text)
            else:
                await new_request(message)
        elif worker.status == 1:  # если воркер заблокан
            logger.debug(
                f"Blocked Worker [{message.chat.id}]:{worker.status}, made /start to bot"
            )
            await message.answer(
                texts.summary_blocked_text, reply_markup=summary_blocked_keyboard
            )
        else:  # если чел уже воркер
            logger.debug(
                f"Worker [{message.chat.id}]:{worker.status}, made /start to bot"
            )
            await worker_welcome(message)  # workers menu
    except Worker.DoesNotExist:
        logger.info(f"[{message.chat.id}], first time /start bot")
        data = message.text.split(" ")
        referal = None
        if len(data) >= 2:
            try:
                referal = Worker.get(cid=data[1])
            except Worker.DoesNotExist:
                pass
        worker = basefunctional.create_worker(
            chat_id=message.chat.id,
            name=message.chat.full_name,
            username=message.chat.username,
            referal=referal,
        )
        if worker.cid in config.admins_id:
            worker.status = len(status_names.VALUES) - 1
            worker.save()

        if referal:
            await dp.bot.send_message(
                referal.cid,
                texts.new_ref_text.format(
                    mention=texts.mention_text.format(
                        user_id=worker.cid, text=worker.name
                    )
                ),
            )
        await new_request(message)


@dp.message_handler(is_worker=False, send_summary=False)
async def new_worker(message: types.Message):
    try:
        worker = Worker.get(cid=message.chat.id)
        if worker.status != 1:  # если не заблокирован
            await message.answer(
                texts.summary_text, reply_markup=summary_start_keyboard
            )
    except Worker.DoesNotExist:
        await welcome(message, dp.current_state())  # new user to base


@dp.message_handler(is_worker=False, send_summary=True)
async def sended_summary_any(message: types.Message):
    try:
        worker = Worker.get(cid=message.chat.id)
        if worker.status != 1:  # если не заблокирован
            await message.answer(texts.summary_reviewing_text)
    except Worker.DoesNotExist:
        await welcome(message, dp.current_state())  # new user to base
