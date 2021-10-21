from asyncio import sleep

from aiogram import types
from loguru import logger

from customutils.models import Worker, EscortUser
from customutils.datefunc import datetime_local_now

from loader import dp
from data import payload
from data.keyboards import escort_keyboard, escort_mamonths_keyboard
from utils.executional import get_correct_str


@dp.message_handler(regexp="эскорт", is_worker=True, state="*")
async def casino_info(message: types.Message):
    worker = Worker.get(cid=message.from_user.id)
    await message.answer(
        payload.escort_text.format(
            worker_id=worker.uniq_key,
        ),
        reply_markup=escort_keyboard,
        disable_web_page_preview=True,
    )


def format_mamont(user: EscortUser) -> str:
    return payload.esc_mamonth_info_text.format(
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
        await query.message.answer(payload.no_mamonths_text)
    else:
        mamonths = worker.esc_users[page * row_width - row_width : page * row_width]
        if not mamonths:
            await query.message.answer(payload.no_mamonths_text)
            logger.debug(f"[{query.from_user.id}] - has no mamonths")
            return

        mamonths_text = "\n".join(map(format_mamont, mamonths))

        data = {
            "text": payload.all_esc_mamonths_text.format(
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
