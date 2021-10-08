from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import RegexpCommandsFilter
from loguru import logger

from customutils.models import CasinoUser, CasinoPayment, Worker
from customutils.datefunc import datetime_local_now

from config import config, MinDepositValues, html_style_url
from loader import dp, casino_bot
from data import payload
from data.states import Casino
from data.keyboards import *
from utils.alert import alert_users
from utils.executional import get_correct_str, get_casino_mamonth_info


@dp.message_handler(  # ru and en - C word
    RegexpCommandsFilter(regexp_commands=["c(\d+)", "с(\d+)"]),
    state="*",
    is_worker=True,
)
async def casino_command(message: types.Message, worker: Worker, regexp_command):
    mb_id = regexp_command.group(1)
    try:
        user = CasinoUser.get(id=mb_id)  # can get by str
    except CasinoUser.DoesNotExist:
        await message.reply("Такого мамонта не существует!")
        logger.debug(
            f"Mamonth [{mb_id}] that worker [{message.chat.id}] want see does not exist."
        )
        return

    # try:
    #     worker = Worker.get(cid=message.chat.id)
    # except Worker.DoesNotExist:
    #     logger.debug(f"/c Worker [{message.chat.id}] does not exist in base.")
    #     return

    if user.owner == worker:
        logger.debug(f"/c Worker [{message.chat.id}] get mamonth info.")
    elif user.status >= 4:  # if user support and upper
        logger.debug(
            f"/c Admin:{user.status} [{message.chat.id}] get not self mamonth info"
        )
    else:
        logger.warning(f"/c Worker [{message.chat.id}] try get different mamonth!")
        return

    text, markup = await get_casino_mamonth_info(worker, user)

    await message.answer(
        text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "updateinfo", is_worker=True, state="*"
)
async def update_mamonth_info(query: types.CallbackQuery, worker: Worker):
    mb_id = query.data.split("_")[1]
    try:
        user = CasinoUser.get(id=mb_id)  # can get by str
    except CasinoUser.DoesNotExist:
        logger.debug(
            f":update_info: Mamonth [{mb_id}] that worker [{query.from_user.id}] want see does not exist."
        )
        return

    if user.owner != worker:
        logger.warning(
            f":update_info: Worker [{message.chat.id}] try get different mamonth!"
        )
        return

    text, markup = await get_casino_mamonth_info(worker, user)

    await query.message.edit_text(
        text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "updatefart",
    state="*",
    is_worker=True,
)
async def update_mamonth_fart(query: types.CallbackQuery, worker: Worker):
    mb_id = query.data.split("_")[1]
    try:
        user = CasinoUser.get(id=mb_id)  # can get by str
    except CasinoUser.DoesNotExist:
        logger.debug(
            f"Mamonth [{mb_id}] that worker [{query.from_user.id}] want update fart does not exist."
        )

    if user.owner != worker:
        logger.warning(
            f":update_info: Worker [{message.chat.id}] try get different mamonth!"
        )
        return

    user.fort_chance = int(  # update fort chance
        100 if user.fort_chance == 0 else 50 if user.fort_chance == 100 else 0
    )
    user.save()

    text, markup = await get_casino_mamonth_info(worker, user)

    await query.message.edit_text(
        text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "updatemin",
    state="*",
    is_worker=True,
)
async def update_mamonth_fart(query: types.CallbackQuery, worker: Worker):
    mb_id = query.data.split("_")[1]
    try:
        user = CasinoUser.get(id=mb_id)  # can get by str
    except CasinoUser.DoesNotExist:
        logger.debug(
            f"Mamonth [{mb_id}] that worker [{query.from_user.id}] want update fart does not exist."
        )

    if user.owner != worker:
        logger.warning(
            f":update_info: Worker [{message.chat.id}] try get different mamonth!"
        )
        return

    try:
        index = MinDepositValues.index(user.min_deposit) + 1
    except ValueError:
        index = 0

    if index > len(MinDepositValues) - 1:
        index = 0

    user.min_deposit = MinDepositValues[index]
    user.save()

    text, markup = await get_casino_mamonth_info(worker, user)

    await query.message.edit_text(
        text,
        reply_markup=markup,
    )


def format_mamont(user: CasinoUser) -> str:
    return payload.small_mamonth_info_text.format(
        mid=user.id,
        cid=user.cid,
        name=user.fullname,
        balance=user.balance,
        fortune="Вкл"
        if user.fort_chance == 100
        else "Выкл"
        if user.fort_chance == 0
        else f"{user.fort_chance} %",
    )


@dp.callback_query_handler(text="mamonths_cas", state="*", is_worker=True)
async def all_mamonths_command(query: types.CallbackQuery, worker: Worker):
    page = 1  # raise if shit
    row_width = 20

    # worker = Worker.get(cid=query.from_user.id)
    mamonths_count = worker.cas_users.count()
    localnow = datetime_local_now()
    timenow = localnow.strftime("%H:%M, %S cек")

    if mamonths_count == 0:
        await query.message.answer(payload.no_mamonths_text)
    else:  # format mamonth its a def on 176 line mb not()
        cusers = list(worker.cas_users)[::-1]
        mamonths = cusers[page * row_width - row_width : page * row_width]
        if not mamonths:
            await query.message.answer(payload.no_mamonths_text)
            return  # logg plz

        mamonths_text = "\n".join(
            map(
                format_mamont,
                mamonths,
            )
        )
        await query.message.answer(
            payload.all_mamonths_text.format(
                mamonths_plur=get_correct_str(
                    mamonths_count, "Мамонт", "Мамонта", "Мамонтов"
                ),
                all_mamonths=mamonths_text,
                time=timenow,
            ),
            reply_markup=casino_mamonths_keyboard(
                mamonths_count, page=page, row_width=row_width
            ),
        )
        logger.debug("Got mamonths list.")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "updatemamonths", state="*", is_worker=True
)
async def cas_mamonths_info(query: types.CallbackQuery, worker: Worker):
    page = int(query.data.split("_")[1])  # raise if shit
    row_width = 20
    # await query.answer("Вывожу!")

    # worker = Worker.get(cid=query.from_user.id)
    mamonths_count = worker.cas_users.count()
    localnow = datetime_local_now()
    timenow = localnow.strftime("%H:%M, %S cек")
    if mamonths_count == 0:
        await query.message.edit_text(payload.no_mamonths_text)
    else:  # format mamonth its a def on 176 line mb not()
        cusers = list(worker.cas_users)[::-1]
        mamonths = cusers[page * row_width - row_width : page * row_width]
        if not mamonths:
            await query.message.answer(payload.no_mamonths_text)
            return  # logg plz

        mamonths_text = "\n".join(
            map(
                format_mamont,
                mamonths,
            )
        )

        await query.message.edit_text(
            payload.all_mamonths_text.format(
                mamonths_plur=get_correct_str(
                    mamonths_count, "Мамонт", "Мамонта", "Мамонтов"
                ),
                all_mamonths=mamonths_text,
                time=timenow,
            ),
            reply_markup=casino_mamonths_keyboard(
                mamonths_count, page=page, row_width=row_width
            ),
        )
        logger.debug("Got mamonths list.")


@dp.callback_query_handler(text="all_alerts_cas", state="*", is_worker=True)
async def cas_mamonths_alert(query: types.CallbackQuery):
    await query.message.answer_photo(html_style_url, caption=payload.cas_alert_text)
    await Casino.alert.set()
    await query.answer("Лови.")


@dp.message_handler(state=Casino.alert)  # is_worker=True
async def cas_mamonths_alert_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await message.answer(message.text, reply_markup=serv_alaccept_keyboard)
    await Casino.alert_true.set()


@dp.callback_query_handler(text="alert_accept", state=Casino.alert_true, is_worker=True)
async def cas_alert_true(query: types.CallbackQuery, worker: Worker, state: FSMContext):
    # print(alert_users([[1, 2]], casino_bot))
    # worker = Worker.get(cid=query.from_user.id)
    async with state.proxy() as data:
        text = data["text"]
    await state.finish()

    msg_len = worker.cas_users.count()
    async for answer in alert_users(
        text, map(lambda usr: usr.cid, worker.cas_users), casino_bot
    ):
        await sleep(0.3)  # delay
        if answer["network_count"] > 0:
            await query.message.edit_text("Телеграмм не отвечает на запрос :(")
            return
        elif answer["cantparse_count"] > 0:
            await query.message.edit_text("Что-то с текстом, не парсит :(")
            return
        elif answer["internal_count"] > 0:
            await query.message.edit_text("Какая-то ошибка в рассылке, сообщи кодеру!")
            return
        else:
            try:
                localnow = datetime_local_now()
                timenow = localnow.strftime("%H:%M, %S cек")
                await query.message.edit_text(
                    payload.cas_alsend_text.format(
                        text=text,
                        msg_count=answer["msg_count"],
                        msg_len=msg_len,
                        timenow=timenow,
                    )
                )
            except Exception as ex:
                logger.exception(ex)

    await query.message.reply("Рассылка завершилась.")
    logger.debug("Alert done.")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "payaccept", is_worker=True, state="*"
)
async def accept_pay(query: types.CallbackQuery):
    pay_id = query.data.split("_")[1]
    try:
        pay = CasinoPayment.get(id=pay_id)
        pay.done = 2
        pay.save()

        await query.message.edit_text(
            query.message.parse_entities() + "\n\nВы приняли заявку"
        )
        logger.debug("Pay accepted.")
        await query.answer("Принял")
    except CasinoPayment.DoesNotExist:
        await query.answer("Ошибка!")


@dp.callback_query_handler(text="mindep_cas", state="*", is_worker=True)
async def minimal_deposit_casino(query: types.CallbackQuery, worker: Worker):
    try:
        index = MinDepositValues.index(worker.casino_min) + 1
    except ValueError:
        index = 0

    if index > len(MinDepositValues) - 1:
        index = 0

    worker.casino_min = MinDepositValues[index]
    worker.save()

    await query.message.edit_text(
        payload.casino_text.format(
            worker_id=worker.uniq_key,
            pay_cards="\n".join(
                map(
                    lambda c: f"&#127479;&#127482; {c[1:]}"
                    if c[0] == "r"
                    else f"&#127482;&#127462; {c[1:]}",
                    config("fake_cards"),
                )
            ),
            pay_qiwis="\n".join(
                map(
                    lambda c: f"&#127479;&#127482; {c[1:]}"
                    if c[0] == "r"
                    else f"&#127482;&#127462; {c[1:]}",
                    config("fake_numbers"),
                )
            ),
        ),
        reply_markup=casino_keyboard(worker.casino_min),
        disable_web_page_preview=True,
    )
    logger.debug(f"Worker [{worker.cid}] update min casino deposit succesfully")

    await query.answer("Изменил!")
