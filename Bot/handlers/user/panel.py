from time import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types.input_file import InputFile
from aiogram.utils.emoji import emojize
from aiogram.utils.deep_linking import get_start_link
from loguru import logger

from loader import dp, config, status_names
from utils import basefunctional
from models import Worker, Profit
from customutils.datefunc import datetime_local_now
from data.texts import (
    zap_text,
    worker_menu_text,
    referral_system_text,
    rules_text,
    about_project_text,
)
from data.keyboards import panel_keyboard, about_project_keyboard, menu_keyboard
from utils.executional import get_correct_str, get_work_status
from utils.render import render_profile


async def get_profile_photo(chat_id: int) -> InputFile:
    profile_pictures = await dp.bot.get_user_profile_photos(chat_id)
    photo_path = f"../media/prf{chat_id}.jpg"
    active = False
    if profile_pictures.total_count != 0:
        active = True
        await profile_pictures.photos[0][-1].download(destination_file=photo_path)

    render_profile(photo_path, active)  # make some shit
    return InputFile(photo_path)


@dp.message_handler(
    Text(startswith="профиль", ignore_case=True), is_worker=True, state="*"
)
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
    all_balance = basefunctional.get_profits_sum(worker.id)
    middle_profits = 0
    if len_profits:
        middle_profits = int(all_balance / len_profits)

    logger.debug(
        f"Worker - {query.from_user.id} get profile, {all_balance=} {len_profits=} {middle_profits=}"
    )

    profile_photo = await get_profile_photo(query.from_user.id)

    if config.casino_work:
        work_status = emojize(":full_moon: <b>Всё работает</b>, воркаем!")
    else:
        work_status = emojize(":new_moon: <b>Временно стопворк!</b>")

    await query.message.delete()
    await query.message.answer_photo(
        profile_photo,
        worker_menu_text.format(
            chat_id=query.from_user.id,
            uniq_key=worker.uniq_key,
            status=status_names[worker.status],
            all_balance=all_balance,
            ref_balance=worker.ref_balance,
            middle_profits=middle_profits,
            profits=get_correct_str(len_profits, "профит", "профита", "профитов"),
            in_team=get_correct_str(in_team.days, "день", "дня", "дней"),
            warns=worker.warns,
            team_status=work_status,
        ),
        reply_markup=panel_keyboard(worker.username_hide),
    )


async def worker_welcome(message: types.Message):
    a = time()
    logger.debug(f"Worker - {message.chat.id}, wants get profile")

    worker = Worker.get(cid=message.chat.id)
    worker.username = message.chat.username
    worker.save()  # update worker username
    in_team = datetime_local_now() - worker.registered

    len_profits = worker.profits.count()
    all_balance = basefunctional.get_profits_sum(worker.id)
    middle_profits = 0
    if len_profits:
        middle_profits = int(all_balance / len_profits)

    logger.debug(
        f"Worker - {message.chat.id} get profile, profits all: {all_balance} len: {len_profits} middle: {middle_profits}"
    )

    await message.answer(zap_text, reply_markup=menu_keyboard)

    profile_photo = await get_profile_photo(message.chat.id)

    if config.casino_work:
        work_status = emojize(":full_moon: <b>Всё работает</b>, воркаем!")
    else:
        work_status = emojize(":new_moon: <b>Временно стопворк!</b>")

    await message.answer_photo(
        profile_photo,
        caption=worker_menu_text.format(
            chat_id=message.chat.id,
            uniq_key=worker.uniq_key,
            status=status_names[worker.status],
            all_balance=all_balance,
            ref_balance=worker.ref_balance,
            middle_profits=middle_profits,
            profits=get_correct_str(len_profits, "профит", "профита", "профитов"),
            in_team=get_correct_str(in_team.days, "день", "дня", "дней"),
            warns=worker.warns,
            team_status=work_status,
        ),
        reply_markup=panel_keyboard(worker.username_hide),
    )

    time_to_do = time() - a
    logger.debug(f"worker_welcome:{time_to_do=}")


@dp.message_handler(
    Text(startswith="о проект", ignore_case=True), is_worker=True, state="*"
)
async def project_info(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logger.debug(f"Cancelling state {current_state} in bot project info")
        await state.finish()

    team_profits = Profit.select().count()

    await message.answer(
        about_project_text.format(
            team_start=config.team_start,
            team_name=config.team_name,
            team_profits=team_profits,
            profits_sum=basefunctional.all_profits_sum(),
            services_status=get_work_status(),
        ),
        reply_markup=about_project_keyboard(
            config.outs_link, config.reviews_link, config.workers_link
        ),
    )
    logger.debug(f"Worker - {message.chat.id}, get project info")


@dp.callback_query_handler(text="toggleusername", is_worker=True)
async def toggle_username(query: types.CallbackQuery):
    try:  # @nastyasladost иди в хайд тим пожалуйста)
        worker = Worker.get(cid=query.message.chat.id)
        worker.username_hide = not worker.username_hide
        in_team = datetime_local_now() - worker.registered
        worker.save()
        logger.debug(
            f"Worker - {worker.cid}:{worker.id}, change username hide status to {worker.username_hide}"
        )

        len_profits = worker.profits.count()
        all_balance = basefunctional.get_profits_sum(worker.id)

        middle_profits = 0
        if len_profits:
            middle_profits = int(all_balance / len_profits)

        status = "Скрыли" if worker.username_hide else "Открыли"

        if config.casino_work:
            work_status = emojize(":full_moon: <b>Всё работает</b>, воркаем!")
        else:
            work_status = emojize(":new_moon: <b>Временно стопворк!</b>")

        await query.message.edit_caption(
            worker_menu_text.format(
                chat_id=query.message.chat.id,
                uniq_key=worker.uniq_key,
                status=status_names[worker.status],
                all_balance=all_balance,
                ref_balance=worker.ref_balance,
                middle_profits=middle_profits,
                profits=get_correct_str(len_profits, "профит", "профита", "профитов"),
                in_team=get_correct_str(in_team.days, "день", "дня", "дней"),
                warns=worker.warns,
                team_status=work_status,
            ),
            reply_markup=panel_keyboard(worker.username_hide),
        )
        await query.answer(f"Вы {status} никнейм")
    except Worker.DoesNotExist:
        pass


@dp.callback_query_handler(text="showrules", is_worker=True)
async def show_rules(query: types.CallbackQuery):
    await query.message.answer(rules_text(True))


@dp.callback_query_handler(text="refsystem", is_worker=True)
async def ref_system(query: types.CallbackQuery):
    link = await get_start_link(query.from_user.id)
    await query.message.answer(
        referral_system_text.format(user_id=query.message.chat.id, start_link=link)
    )
