from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loguru import logger

from models import TradingUser, TradingPayment, Worker
from customutils import datetime_local_now
from loader import config, dp, trading_bot
from data.keyboards import *
from data.texts import exact_out_text
from utils.executional import (
    get_trading_info,
)


@dp.message_handler(
    Text(startswith="трейд", ignore_case=True), state="*", is_worker=True
)
async def trading_info(message: types.Message, worker: Worker, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logger.debug(f"Cancelling state {current_state} in bot start")
        await state.finish()

    logger.debug(f"Worker [{message.chat.id}] want get trading info")

    await message.answer(
        get_trading_info(worker.uniq_key),
        disable_web_page_preview=True,
    )

    # await TradingAlert.commands.set() # old deleted from states.py
    logger.debug(f"Worker [{message.chat.id}] get trading info succesfully")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "tdgadd", is_worker=True, state="*"
)
async def accept_pay(query: types.CallbackQuery):
    pay_id = query.data.split("_")[1]
    try:
        pay = TradingPayment.get(id=pay_id)
        check_time = config.qiwi_check_time * 2  # - 3 just for somethink)
        exact_time = (datetime_local_now() - pay.created).seconds

        logger.debug(f"{check_time=} (qiwi_check_time * 2), {exact_time=}")

        if pay.done == 1:
            await query.message.edit_text(
                query.message.parse_entities() + "\n\n<b>Мамонт уже оплатил заявку!</b>"
            )
            return
        elif exact_time >= check_time:
            pay.done = 2
            pay.save()
        elif exact_time <= check_time:
            await query.answer(f"Жди еще {check_time - exact_time} секунд!")
            return
        else:
            await query.answer(f"Зови кодера)")
            return

        await query.message.edit_text(
            query.message.parse_entities() + "\n\n<i>Вы оплатили заявку</i>"
        )
        logger.debug(f"Trading Pay {pay_id=} accepted!")
        await query.answer("Принял!")
    except TradingPayment.DoesNotExist:
        await query.answer("Ошибка!")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "tdgout", is_worker=True, state="*"
)
async def accept_out(query: types.CallbackQuery):
    user_id = int(query.data.split("_")[1])  # must be int! - TradingUser.id
    try:
        user = TradingUser.get(id=user_id)

        await trading_bot.send_message(
            user.cid,
            exact_out_text.format(
                amount=user.balance,
            ),
        )

        user.balance = 0
        user.save()

        await query.message.edit_text(
            query.message.parse_entities() + "\n\n<i>Успешный вывод!</i>"
        )
    except TradingUser.DoesNotExist:
        await query.answer("Зови кодера пж! Ошибка!!!!")
