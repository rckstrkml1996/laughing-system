from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.emoji import emojize
from loguru import logger

from loader import dp, db_commands
from config import config
from config import StatusNames
from customutils.models import Worker, Profit
from customutils.datefunc import datetime_local_now
from data import payload
from data.keyboards import *
from utils.executional import get_correct_str, get_work_status


@dp.message_handler(regexp="профил", is_worker=True, state="*")
async def worker_profile(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logger.debug(f"Cancelling state {current_state} in bot profile")
        await state.finish()

    await worker_welcome(message)


@dp.callback_query_handler(text="menu", is_worker=True, state="*")
async def worker_profile_callback(query: types.CallbackQuery, worker: Worker):
    logger.debug(f"Worker - {query.from_user.id}, wants back to profile")

    # worker.username = query.from_user.username
    # worker.save()  # update worker username
    in_team = datetime_local_now() - worker.registered

    len_profits = worker.profits.count()
    all_balance = db_commands.get_profits_sum(worker.id)
    middle_profits = 0
    if len_profits:
        middle_profits = int(all_balance / len_profits)

    logger.debug(
        f"Worker - {query.from_user.id} get profile, {all_balance=} {len_profits=} {middle_profits=}"
    )

    await query.message.edit_text(
        payload.worker_menu_text.format(
            chat_id=query.from_user.id,
            status=StatusNames[worker.status],
            all_balance=all_balance,
            ref_balance=worker.ref_balance,
            middle_profits=middle_profits,
            profits=get_correct_str(len_profits, "профит", "профита", "профитов"),
            in_team=get_correct_str(in_team.days, "день", "дня", "дней"),
            warns=0,
            team_status=emojize(":full_moon: <b>Всё работает</b>, воркаем!"),
        ),
        reply_markup=panel_keyboard(worker.username_hide),
    )


async def worker_welcome(message: types.Message):
    logger.debug(f"Worker - {message.chat.id}, wants get profile")

    worker = Worker.get(cid=message.chat.id)
    worker.username = message.chat.username
    worker.save()  # update worker username
    in_team = datetime_local_now() - worker.registered

    len_profits = worker.profits.count()
    all_balance = db_commands.get_profits_sum(worker.id)
    middle_profits = 0
    if len_profits:
        middle_profits = int(all_balance / len_profits)

    logger.debug(
        f"Worker - {message.chat.id} get profile, profits all: {all_balance} len: {len_profits} middle: {middle_profits}"
    )

    await message.answer(emojize(":zap:"), reply_markup=menu_keyboard)
    await message.answer(
        payload.worker_menu_text.format(
            chat_id=message.chat.id,
            status=StatusNames[worker.status],
            all_balance=all_balance,
            ref_balance=worker.ref_balance,
            middle_profits=middle_profits,
            profits=get_correct_str(len_profits, "профит", "профита", "профитов"),
            in_team=get_correct_str(in_team.days, "день", "дня", "дней"),
            warns=0,
            team_status=emojize(":full_moon: <b>Всё работает</b>, воркаем!"),
        ),
        reply_markup=panel_keyboard(worker.username_hide),
    )


@dp.message_handler(regexp="проект", is_worker=True, state="*")
async def project_info(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logger.debug(f"Cancelling state {current_state} in bot project info")
        await state.finish()

    team_profits = Profit.select().count()

    await message.answer(
        payload.about_project_text.format(
            team_start=config("team_start"),
            team_profits=team_profits,
            profits_sum=db_commands.all_profits_sum(),
            services_status=get_work_status(),
        ),
        reply_markup=about_project_keyboard,
    )
    logger.debug(f"Worker - {message.chat.id}, get project info")


@dp.callback_query_handler(text="toggleusername", is_worker=True)
async def toggle_username(query: types.CallbackQuery):
    try:
        worker = Worker.get(cid=query.message.chat.id)
        worker.username_hide = not worker.username_hide
        in_team = datetime_local_now() - worker.registered
        worker.save()
        logger.debug(
            f"Worker - {worker.cid}:{worker.id}, change username hide status to {worker.username_hide}"
        )

        len_profits = worker.profits.count()
        all_balance = db_commands.get_profits_sum(worker.id)

        middle_profits = 0
        if len_profits:
            middle_profits = int(all_balance / len_profits)

        status = "Скрыли" if worker.username_hide else "Открыли"

        await query.message.edit_text(
            payload.worker_menu_text.format(
                chat_id=query.message.chat.id,
                status=StatusNames[worker.status],
                all_balance=all_balance,
                ref_balance=worker.ref_balance,
                middle_profits=middle_profits,
                profits=get_correct_str(len_profits, "профит", "профита", "профитов"),
                in_team=get_correct_str(in_team.days, "день", "дня", "дней"),
                warns=0,
                team_status=emojize(":full_moon: <b>Всё работает</b>, воркаем!"),
            ),
            reply_markup=panel_keyboard(worker.username_hide),
        )
        await query.answer(f"Вы {status} никнейм")
    except Worker.DoesNotExist:
        pass


@dp.callback_query_handler(text="showrules", is_worker=True)
async def show_rules(query: types.CallbackQuery):
    await query.message.answer(payload.rules_text(True))


@dp.callback_query_handler(text="refsystem", is_worker=True)
async def ref_system(query: types.CallbackQuery):
    await query.message.answer(
        payload.referral_system_text.format(user_id=query.message.chat.id)
    )
