from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from customutils.models import Worker, CasinoUser
from loguru import logger

from loader import dp, casino_bot
from data import payload
from data.keyboards import *
from data.states import Alert


@dp.message_handler(commands=["alert", "alerts"], admins_chat=True, is_admin=True, state="*")
async def alert_command(message: types.Message):
    logger.debug(f"Admin [{message.from_user.id}] called alert command")
    await message.answer(payload.alert_text, reply_markup=alert_keyboard)


# alert bot
@dp.callback_query_handler(text="alert_bot", admins_chat=True, is_admin=True)
async def alert_bot(query: types.CallbackQuery):
    await query.message.edit_text(
        payload.make_alert_text.format(bot_type="Основного бота")
    )
    await Alert.bot.set()


@dp.message_handler(state=Alert.bot, admins_chat=True)
async def text_alert_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await message.answer(
        payload.alert_accept_text.format(text=message.text),
        reply_markup=alert_accept_keyboard,
    )
    await Alert.bot_accept.set()


@dp.callback_query_handler(text="alert_edit", state=Alert.bot_accept, admins_chat=True)
async def alert_edit(query: types.CallbackQuery):
    await query.message.edit_text(
        payload.edit_alert_text.format(bot_type="Основного бота")
    )
    logger.debug("Admin changing alert text")
    await Alert.bot.set()


@dp.callback_query_handler(
    text="alert_accept", state=Alert.bot_accept, admins_chat=True
)
async def alert_accepted(query: types.CallbackQuery, state: FSMContext):
    workers = Worker.select()
    len_users = workers.count()
    msg_count = 0
    blocked_count = 0
    not_found_count = 0

    for worker in workers:
        try:
            async with state.proxy() as data:
                await dp.bot.send_message(worker.cid, data["text"])
            await query.message.edit_text(
                payload.alert_start_text.format(
                    len_users=len_users,
                    msg_count=msg_count,
                    blocked_count=blocked_count,
                    not_found_count=not_found_count,
                )
            )
            msg_count += 1
        except ChatNotFound:
            not_found_count += 1
        except BotBlocked:
            blocked_count += 1
        await sleep(0.2)

    await query.message.edit_text(
        payload.alert_start_text.format(
            len_users=len_users,
            msg_count=msg_count,
            blocked_count=blocked_count,
            not_found_count=not_found_count,
        )
    )
    await query.message.reply(payload.alert_complete_text)
    logger.debug("Alert finished")
    await state.finish()


# alert casino


@dp.callback_query_handler(text="alert_casino", admins_chat=True, is_admin=True)
async def alert_casino(query: types.CallbackQuery):
    await query.message.edit_text(
        payload.make_alert_text.format(bot_type="Казино ботов")
    )
    await Alert.casino.set()


@dp.message_handler(state=Alert.casino, admins_chat=True)
async def text_alert_casino(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await message.answer(
        payload.alert_accept_text.format(text=message.text),
        reply_markup=alert_accept_keyboard,
    )
    await Alert.casino_accept.set()


@dp.callback_query_handler(
    text="alert_edit", state=Alert.casino_accept, admins_chat=True
)
async def alert_edit(query: types.CallbackQuery):
    await query.message.edit_text(payload.edit_alert_text.format(bot_type="Казиков"))
    await Alert.casino.set()


@dp.callback_query_handler(
    text="alert_accept", state=Alert.casino_accept, admins_chat=True
)
async def alert_accepted(query: types.CallbackQuery, state: FSMContext):
    users = CasinoUser.select()
    len_users = users.count()
    msg_count = 0
    blocked_count = 0
    not_found_count = 0

    for user in users:
        try:
            async with state.proxy() as data:
                await casino_bot.send_message(user.cid, data["text"])
            await query.message.edit_text(
                payload.alert_start_text.format(
                    len_users=len_users,
                    msg_count=msg_count,
                    blocked_count=blocked_count,
                    not_found_count=not_found_count,
                )
            )
            msg_count += 1
        except ChatNotFound:
            not_found_count += 1
        except BotBlocked:
            blocked_count += 1
        await sleep(0.2)

    await query.message.edit_text(
        payload.alert_start_text.format(
            len_users=len_users,
            msg_count=msg_count,
            blocked_count=blocked_count,
            not_found_count=not_found_count,
        )
    )
    await query.message.reply(payload.alert_complete_text)
    logger.debug("Alert finished")

    await state.finish()


# alert escort
@dp.callback_query_handler(text="alert_escort", admins_chat=True, is_admin=True)
async def alert_escort(query: types.CallbackQuery):
    await query.message.edit_text(payload.make_alert_text.format(bot_type="Эскорта"))
    await Alert.escort.set()


@dp.message_handler(state=Alert.escort, admins_chat=True)
async def text_alert_escort(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await message.answer(
        payload.alert_accept_text.format(text=message.text),
        reply_markup=alert_accept_keyboard,
    )
    await Alert.escort_accept.set()


@dp.callback_query_handler(
    text="alert_edit", state=Alert.escort_accept, admins_chat=True
)
async def alert_edit(query: types.CallbackQuery):
    await query.message.edit_text(payload.edit_alert_text.format(bot_type="Эскорта"))
    await Alert.escort.set()


# alert trading


@dp.callback_query_handler(text="alert_trading", admins_chat=True, is_admin=True)
async def alert_trading(query: types.CallbackQuery):
    await query.message.edit_text(payload.make_alert_text.format(bot_type="Трейдинга"))
    await Alert.trading.set()


@dp.message_handler(state=Alert.trading, admins_chat=True)
async def text_alert_trading(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await message.answer(
        payload.alert_accept_text.format(text=message.text),
        reply_markup=alert_accept_keyboard,
    )
    await Alert.trading_accept.set()


@dp.callback_query_handler(
    text="alert_edit", state=Alert.trading_accept, admins_chat=True
)
async def alert_edit(query: types.CallbackQuery):
    await query.message.edit_text(payload.edit_alert_text.format(bot_type="Трейдинга"))
    await Alert.trading.set()


# reject all alerts
@dp.callback_query_handler(
    text="alert_reject",
    state=[
        Alert.bot_accept,
        Alert.casino_accept,
        Alert.escort_accept,
        Alert.trading_accept,
    ],
    admins_chat=True,
)
async def alert_reject(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(payload.alert_reject_text)
    await state.finish()
