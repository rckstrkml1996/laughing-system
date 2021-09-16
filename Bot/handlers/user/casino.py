import re
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher.filters import RegexpCommandsFilter
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from loguru import logger

from customutils.models import CasinoUser, CasinoUserHistory, Worker
from customutils.datefunc import datetime_local_now

from config import config, html_style_url
from loader import dp, db_commands  # casino_bot
from data import payload
from data.states import Casino
from data.keyboards import *
from utils.executional import get_correct_str, get_casino_mamonth_info


@dp.message_handler(  # ru and en - C word
    RegexpCommandsFilter(regexp_commands=["c(\d+)", "с(\d+)"]),
    state="*",
    is_worker=True,
)
async def casino_command(message: types.Message, regexp_command):
    mb_id = regexp_command.group(1)
    # if mb_id.isdigit():
    try:
        user = CasinoUser.get(id=mb_id)  # can get by str
    except CasinoUser.DoesNotExist:
        await message.reply("Такого мамонта не существует!")
        logger.debug(
            f"Mamonth [{mb_id}] that worker [{message.chat.id}] want see does not exist."
        )
        return

    try:
        worker = Worker.get(cid=message.chat.id)
    except Worker.DoesNotExist:
        logger.debug(f"/c Worker [{message.chat.id}] does not exist in base.")
        return

    if user.owner != worker:
        logger.warning(f"/c Worker [{message.chat.id}] try get different mamonth!")
        return

    text, markup = await get_casino_mamonth_info(worker, user)

    await message.answer(
        text,
        reply_markup=markup,
    )

    # else:
    #     await message.reply("Команда введена неправильно!")


@dp.message_handler(regexp="казин", state="*", is_worker=True)
async def casino_info(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logger.debug(f"Cancelling state {current_state} in bot start")
        await state.finish()

    logger.debug(f"Worker [{message.chat.id}] want get casino info")
    try:
        worker = Worker.get(cid=message.chat.id)
        await message.answer(
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
            reply_markup=casino_keyboard,
            disable_web_page_preview=True,
        )
        # await Casino.commands.set()
        logger.debug(f"Worker [{message.chat.id}] get casino info succesfully")
    except Worker.DoesNotExist:
        logger.debug(f"Worker [{message.chat.id}] in casino info does not exist")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "updateinfo", is_worker=True, state="*"
)
async def update_mamonth_info(query: types.CallbackQuery):
    mb_id = query.data.split("_")[1]
    try:
        user = CasinoUser.get(id=mb_id)  # can get by str
    except CasinoUser.DoesNotExist:
        logger.debug(
            f":update_info: Mamonth [{mb_id}] that worker [{query.from_user.id}] want see does not exist."
        )
        return

    try:
        worker = Worker.get(cid=query.from_user.id)
    except Worker.DoesNotExist:
        logger.debug(
            f":update_info: Worker [{message.chat.id}] does not exist in base."
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
async def update_mamonth_fart(query: types.CallbackQuery):
    mb_id = query.data.split("_")[1]
    try:
        user = CasinoUser.get(id=mb_id)  # can get by str
    except CasinoUser.DoesNotExist:
        logger.debug(
            f"Mamonth [{mb_id}] that worker [{query.from_user.id}] want update fart does not exist."
        )

    try:
        worker = Worker.get(cid=query.from_user.id)
    except Worker.DoesNotExist:
        logger.debug(f":updatefart: Worker [{message.chat.id}] does not exist in base.")
        return

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
async def all_mamonths_command(query: types.CallbackQuery):
    row_width = 20

    worker = Worker.get(cid=query.from_user.id)
    mamonths_count = worker.cas_users.count()
    localnow = datetime_local_now()
    timenow = localnow.strftime("%H:%M, %S cек")

    if mamonths_count == 0:
        await query.message.answer(payload.no_mamonths_text)
    else:  # format mamonth its a def on 176 line mb not()
        mamonths = worker.cas_users[1 * row_width - row_width : 1 * row_width]
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
                mamonths_count, page=1, row_width=row_width
            ),
        )
        logger.debug("Got mamonths list.")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "updatemamonths", state="*", is_worker=True
)
async def cas_mamonths_info(query: types.CallbackQuery):
    page = int(query.data.split("_")[1])  # raise if shit
    row_width = 20
    # await query.answer("Вывожу!")

    worker = Worker.get(cid=query.from_user.id)
    mamonths_count = worker.cas_users.count()
    localnow = datetime_local_now()
    timenow = localnow.strftime("%H:%M, %S cек")
    if mamonths_count == 0:
        await query.message.edit_text(payload.no_mamonths_text)
    else:  # format mamonth its a def on 176 line mb not()
        mamonths = worker.cas_users[1 * row_width - row_width : 1 * row_width]
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


@dp.message_handler(state=Casino.alert)  # is_worker=True
async def cas_mamonths_alert_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await message.answer(message.text, reply_markup=serv_alaccept_keyboard)
    await Casino.alert_true.set()


@dp.callback_query_handler(text="alert_accept", state=Casino.alert_true, is_worker=True)
async def cas_alert_true(query: types.CallbackQuery, state: FSMContext):
    worker = Worker.get(cid=query.from_user.id)
    async with state.proxy() as data:
        await state.finish()
        msg_count = 0
        msg_len = worker.cas_users.count()
        await query.message.edit_text(
            payload.cas_alsend_text.format(
                text=data["text"], msg_count=msg_count, msg_len=msg_len
            )
        )
        for user in worker.cas_users:
            try:
                await casino_bot.send_message(user.cid, data["text"])
                msg_count += 1
                await sleep(0.5)
            except (ChatNotFound, BotBlocked):
                continue
            except:
                continue

            if msg_count % 5 == 0:
                await query.message.edit_text(
                    payload.cas_alsend_text.format(
                        text=data["text"], msg_count=msg_count, msg_len=msg_len
                    )
                )
                await sleep(0.3)

    await sleep(0.2)
    try:
        await query.message.edit_text(
            payload.cas_alsend_text.format(
                text=data["text"], msg_count=msg_count, msg_len=msg_len
            )
        )
    except:
        pass
    logger.debug("Alert done.")


# async def edit_balance(message: types.Message, user: CasinoUser, match):
#     user.balance = int(match.group(2))
#     user.save()
#     await message.answer("Изменил баланс!")


# # @dp.message_handler(commands="msg", state=Casino.commands, is_worker=True)
# # async def cas_mamonth_msg(message: types.Message):
# #     await match_command(message, r"\/msg (c\d+|\d+);(.+)", send_msg_command)


# @dp.message_handler(commands="bal", state=Casino.commands, is_worker=True)
# async def cas_mamonth_bal(message: types.Message):
#     await match_command(message, r"\/bal (c\d+|\d+);(\d+)", edit_balance)


# # @dp.message_handler(commands="info", state=Casino.commands, is_worker=True)
# # async def cas_mamonth_info(message: types.Message):
# #     await match_command(message, r"\/info (c\d+|\d+)", send_info_about_mamonth)


# async def change_fart_mamonth(message: types.Message, user: CasinoUser, match):


# @dp.message_handler(commands="fart", state=Casino.commands, is_worker=True)
# async def cas_fart_command(message: types.Message):
#     await match_command(message, r"\/fart (c\d+|\d+)", change_fart_mamonth)


# async def delete_mamonth(message: types.Message, user: CasinoUser, match):


# @dp.message_handler(commands="del", state=Casino.commands, is_worker=True)
# async def cas_fart_command(message: types.Message):
#     await match_command(message, r"\/del (c\d+|\d+)", delete_mamonth)


# @dp.callback_query_handler(text="my_frazes", state=Casino.commands, is_worker=True)
# async def cas_mamonths_phrazes(query: types.CallbackQuery):
#     await query.answer("Работаю хули")


# @dp.callback_query_handler(text="my_promos", state=Casino.commands, is_worker=True)
# async def cas_mamonths_promos(query: types.CallbackQuery):
#     await query.answer("Работаю")


# @dp.callback_query_handler(text="my_delete_all", state=Casino.commands, is_worker=True)
# async def cas_mamonths_delete(query: types.CallbackQuery):
#     await query.answer("Работаю")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "payaccept", is_worker=True, state="*"
)
async def accept_pay(query: types.CallbackQuery):
    pay_id = query.data.split("_")[1]
    try:
        pay = CasinoPayment.get(id=pay_id)
        pay.done = 1
        pay.save()

        await query.message.edit_text(
            query.message.parse_entities() + "\n\nВы приняли заявку"
        )
        logger.debug("Pay accepted.")
        await query.answer("Принял")
    except CasinoPayment.DoesNotExist:
        await query.answer("Ошибка!")
