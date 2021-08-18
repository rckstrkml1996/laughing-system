from aiogram import types
from aiogram.utils.emoji import emojize

from loader import dp, db_commands
from config import config
from config import StatusNames, team_start
from customutils.models import Worker, Profit
from customutils.datefunc import datetime_local_now
from data import payload
from data.keyboards import *
from utils.executional import get_correct_str, get_work_status


@dp.callback_query_handler(text="menu", is_worker=True)
async def worker_menu(query: types.CallbackQuery):
    worker = Worker.get(cid=query.message.chat.id)
    in_team = datetime_local_now().replace(tzinfo=None) - worker.registered

    len_profits = worker.profits.count()
    all_balance = db_commands.get_profits_sum(worker.id)

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
                middle_profits=int(all_balance / len_profits),
                profits=get_correct_str(
                    len_profits, "профит", "профита", "профитов"),
                in_team=get_correct_str(in_team.days, "день", "дня", "дней"),
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

        len_profits = worker.profits.count()
        all_balance = db_commands.get_profits_sum(worker.id)

        await message.answer(emojize(":zap:"), reply_markup=menu_keyboard)
        await message.answer(
            payload.worker_menu_text.format(
                chat_id=message.chat.id,
                status=StatusNames[worker.status],
                all_balance=all_balance,
                ref_balance=worker.ref_balance,
                middle_profits=int(all_balance / len_profits),
                profits=get_correct_str(
                    len_profits, "профит", "профита", "профитов"),
                in_team=get_correct_str(in_team.days, "день", "дня", "дней"),
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
        team_profits = Profit.select().count()

        await message.answer(
            payload.about_project_text.format(
                team_start=team_start,
                team_profits=team_profits,
                profits_sum=db_commands.get_profits_sum(worker.id),
                services_status=get_work_status()
            ),
            reply_markup=about_project_keyboard
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

        len_profits = worker.profits.count()
        all_balance = db_commands.get_profits_sum(worker.id)

        status = "Скрыли" if worker.username_hide else "Открыли"

        await query.message.edit_text(
            payload.worker_menu_text.format(
                chat_id=query.message.chat.id,
                status=StatusNames[worker.status],
                all_balance=all_balance,
                ref_balance=worker.ref_balance,
                middle_profits=int(all_balance / len_profits),
                profits=get_correct_str(
                    len_profits, "профит", "профита", "профитов"),
                in_team=get_correct_str(in_team.days, "день", "дня", "дней"),
                warns=0,
                team_status=emojize(
                    ":full_moon: <b>Всё работает</b>, воркаем!")
            ),
            reply_markup=panel_keyboard(worker.username_hide),
        )
        await query.answer(f"Вы {status} никнейм")
    except Worker.DoesNotExist:
        pass


@dp.callback_query_handler(text="showrules")
async def show_rules(query: types.CallbackQuery):
    await query.message.answer(
        payload.rules_text(True))


@dp.callback_query_handler(text="refsystem")
async def ref_system(query: types.CallbackQuery):
    await query.message.answer(
        payload.referral_system_text.format(
            user_id=query.message.chat.id))
