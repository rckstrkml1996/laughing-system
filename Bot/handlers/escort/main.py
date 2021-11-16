from asyncio import sleep

from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.dispatcher.filters import Text, RegexpCommandsFilter
from loguru import logger

from models import Worker, EscortUser
from customutils import datetime_local_now
from loader import dp, config
from data.texts import (
    escort_text,
    esc_mamonth_info_text,
    no_mamonths_text,
    all_esc_mamonths_text,
)
from data.keyboards import escort_keyboard, escort_mamonths_keyboard, menu_keyboard
from utils.executional import get_correct_str, get_escort_mamonth_info


@dp.message_handler(
    Text(startswith="эскорт", ignore_case=True), is_worker=True, state="*"
)
async def escort_info(message: types.Message, worker: Worker):
    girl_created = worker.escort_girls.count() >= 1
    await message.answer("ок)", reply_markup=menu_keyboard)
    await message.answer(
        escort_text.format(
            escort_username=config.escort_username,
            escort_sup_username=config.escort_sup_username,
            worker_id=worker.uniq_key,
            reviews_link=config.reviews_link,
        ),
        reply_markup=escort_keyboard(girl_created),
        disable_web_page_preview=True,
    )


@dp.message_handler(  # ru and en - C word
    RegexpCommandsFilter(regexp_commands=["e(\d+)", "е(\d+)"]),
    state="*",
    is_worker=True,
)
async def escort_command(message: types.Message, worker: Worker, regexp_command):
    mb_id = regexp_command.group(1)
    try:
        user = EscortUser.get(id=mb_id)  # can get by str
    except EscortUser.DoesNotExist:
        await message.reply("Такого мамонта не существует!")
        logger.debug(
            f"Mamonth [{mb_id}] that worker [{message.chat.id}] want see does not exist."
        )
        return
    if user.owner == worker:
        logger.debug(f"/e Worker [{message.chat.id}] get mamonth info.")
    elif user.status >= 4:  # if user support and upper
        logger.debug(
            f"/e Admin:{user.status} [{message.chat.id}] get not self mamonth info"
        )
    else:
        logger.warning(f"/e Worker [{message.chat.id}] try get different mamonth!")
        return
    text, markup = get_escort_mamonth_info(user)
    await message.answer(
        text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "escupdateinfo", is_worker=True, state="*"
)
async def update_escort_info(query: types.CallbackQuery, worker: Worker):
    mb_id = query.data.split("_")[1]
    try:
        user = EscortUser.get(id=mb_id)  # can get by str
    except EscortUser.DoesNotExist:
        logger.debug(
            f"Mamonth [{mb_id}] that worker [{query.from_user.id}] want see does not exist."
        )
        return
    if user.owner == worker:
        logger.debug(f"/e Worker [{query.from_user.id}] get mamonth info.")
    elif user.status >= 4:  # if user support and upper
        logger.debug(
            f"/e Admin:{worker.status} [{query.from_user.id}] get not self mamonth info"
        )
    else:
        logger.warning(f"/e Worker [{query.from_user.id}] try get different mamonth!")
        return
    text, markup = get_escort_mamonth_info(user)
    await query.message.edit_text(
        text,
        reply_markup=markup,
    )


def format_mamont(user: EscortUser) -> str:
    return esc_mamonth_info_text.format(
        mid=user.id,
        cid=user.cid,
        name=user.fullname,
        balance=user.balance,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "escupdatemamonths", state="*", is_worker=True
)
async def all_mamonths_command(query: types.CallbackQuery):
    q_page = int(query.data.split("_")[1])
    page = q_page if q_page != 0 else 1
    row_width = 20
    worker = Worker.get(cid=query.from_user.id)
    mamonths_count = worker.esc_users.count()
    localnow = datetime_local_now()
    timenow = localnow.strftime("%H:%M, %S Сек.")
    if mamonths_count == 0:
        await query.message.answer(no_mamonths_text)
    else:
        mamonths = worker.esc_users[page * row_width - row_width : page * row_width]
        if not mamonths:
            await query.message.answer("У тебя нету мамонтов в эскорте!")
            logger.debug(f"[{query.from_user.id}] - has no mamonths")
            return
        mamonths_text = "\n".join(map(format_mamont, mamonths))
        data = {
            "text": all_esc_mamonths_text.format(
                mamonths_plur=get_correct_str(
                    mamonths_count, "Мамонт", "Мамонта", "Мамонтов"
                ),
                all_mamonths=mamonths_text,
                time=timenow,
            ),
            "reply_markup": escort_mamonths_keyboard(
                mamonths_count, page=page, row_width=row_width
            ),
        }
        if q_page == 0:
            await query.message.answer(**data)
            await sleep(0.25)  # some random
            await query.answer("Лови!")
        else:
            await query.message.edit_text(**data)
        logger.debug("Got mamonths list.")
