import re
from datetime import timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.input_file import InputFile
from aiogram.utils.emoji import emojize

from loader import dp
from config import config
from config import StatusNames, Rates, team_start
from data import payload
from data.states import Render, Panel
from data.keyboards import *
from utils.render import *
from utils.executional import datetime_local_now, get_correct_str, get_work_status
from models import Worker, Profit


@dp.callback_query_handler(text="menu", is_worker=True)
async def worker_menu(query: types.CallbackQuery):
    worker = Worker.get(cid=query.message.chat.id)
    in_team = datetime_local_now().replace(tzinfo=None) - worker.registered

    len_profits = len(worker.profits)
    all_balance = sum(map(lambda prft: prft.amount, worker.profits))

    if query.message.photo:  # it cant edit when photo!
        await worker_welcome(query.message)
    else:
        worker.username = query.message.chat.username
        worker.save()  # update worker username
        await query.message.edit_text(
            payload.worker_menu_text.format(
                chat_id=query.message.chat.id,
                status=StatusNames[worker.status],
                all_balance=all_balance,
                ref_balance=worker.ref_balance,
                middle_profits=all_balance / len_profits,
                len_profits=len_profits,
                in_team=f'{in_team.days} {get_correct_str(in_team.days, "день", "дня", "дней")}',
                warns=worker.warns,
                team_status=emojize(
                    ":full_moon: <b>Всё работает</b>, воркаем!")
            ),
            reply_markup=panel_keyboard(worker.username_hide),
        )


@dp.message_handler(regexp="профил")
async def worker_welcome(message: types.Message):
    try:
        worker = Worker.get(cid=message.chat.id)
        worker.username = message.chat.username
        worker.save()  # update worker username
        in_team = datetime_local_now().replace(tzinfo=None) - worker.registered

        await message.answer(emojize(":zap:"), reply_markup=menu_keyboard)
        await message.answer(
            payload.worker_menu_text.format(
                chat_id=message.chat.id,
                status=StatusNames[worker.status],
                all_balance=sum(map(lambda prft: prft.amount, worker.profits)),
                ref_balance=worker.ref_balance,
                middle_profits=0,
                len_profits=len(worker.profits),
                in_team=f'{in_team.days} {get_correct_str(in_team.days, "день", "дня", "дней")}',
                warns=0,
                team_status=emojize(
                    ":full_moon: <b>Всё работает</b>, воркаем!")
            ),
            reply_markup=panel_keyboard(worker.username_hide),
        )
    except Worker.DoesNotExist:
        pass


@dp.message_handler(regexp="проект")
async def project_info(message: types.Message):
    try:
        worker = Worker.get(cid=message.chat.id)
        profits = Profit.select()

        await message.answer(
            payload.about_project_text.format(
                team_start=team_start,
                team_profits=len(profits),
                profits_sum=sum(map(lambda prft: prft.amount, profits)),
                services_status=get_work_status()
            ),
            reply_markup=menu_keyboard
        )
    except Worker.DoesNotExist:
        pass


@dp.callback_query_handler(text="toggleusername")
async def toggle_username(query: types.CallbackQuery):
    try:
        worker = Worker.get(cid=query.message.chat.id)
        worker.username_hide = not worker.username_hide
        in_team = datetime_local_now().replace(tzinfo=None) - worker.registered
        worker.save()
        status = "Скрыли" if worker.username_hide else "Открыли"
        await query.message.edit_text(
            payload.worker_menu_text.format(
                chat_id=query.message.chat.id,
                status=StatusNames[worker.status],
                all_balance=sum(map(lambda prft: prft.amount, worker.profits)),
                ref_balance=worker.ref_balance,
                middle_profits=0,
                len_profits=len(worker.profits),
                in_team=f'{in_team.days} {get_correct_str(in_team.days, "день", "дня", "дней")}',
                warns=0,
                team_status=emojize(
                    ":full_moon: <b>Всё работает</b>, воркаем!")
            ),
            reply_markup=panel_keyboard(worker.username_hide),
        )
        await query.answer(f"Вы {status} никнейм")
    except Worker.DoesNotExist:
        pass
