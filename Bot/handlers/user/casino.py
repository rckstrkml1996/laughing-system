import random
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from loguru import logger
from customutils.models import CasinoUser, CasinoPayment, CasinoUserHistory, Worker
from customutils.datefunc import datetime_local_now

from config import config, html_style_url
from loader import dp, casino_bot
from data import payload
from data.states import Casino
from data.keyboards import *
from utils.executional import random_heart


@dp.message_handler(Text(startswith=["/c", "/с"], ignore_case=True), state="*")
async def casino_command(message: types.Message):
    mb_id = message.text[2:]
    if mb_id.isdigit():
        try:
            user = CasinoUser.get(id=mb_id)  # can get by str

            localnow = datetime_local_now().replace(tzinfo=None)
            timenow = localnow.strftime("%H:%M, %S cек")

            await message.answer(
                payload.casino_mamonth_info.format(
                    smile=random_heart(),
                    uid=user.id,
                    chat_id=user.cid,
                    name=user.fullname,
                    balance=user.balance,
                    time=timenow,
                    fortune="Вкл"
                    if user.fort_chance == 100
                    else "Выкл"
                    if user.fort_chance == 0
                    else f"{user.fort_chance} %",
                ),
                reply_markup=cas_info_keyboard(user.fort_chance, user.id, "PIZDA"),
            )
        except CasinoUser.DoesNotExist:
            logger.debug("Mamonth that worker want see does not exist.")


@dp.message_handler(regexp="казин", state="*", is_worker=True)
async def casino_info(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logger.debug(f"Cancelling state {current_state} in bot start")
        await state.finish()

    logger.debug(f"Worker {message.chat.id} want get casino info")
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
        await Casino.commands.set()
        logger.debug(f"Worker {message.chat.id} get casino info succesfully")
    except Worker.DoesNotExist:
        logger.debug(f"Worker {message.chat.id} in casino info does not exist")


async def match_command(message: types.Message, regex, on_match):
    mtch = re.fullmatch(regex, message.text)
    if mtch:
        try:
            if mtch.group(1)[0] == "c":
                user = CasinoUser.get(id=mtch.group(1)[1:])
            else:
                user = CasinoUser.get(cid=mtch.group(1))

            if user.owner.cid == message.chat.id:
                await on_match(message, user, mtch)
            else:
                await message.answer(payload.no_mamonth_text)
        except CasinoUser.DoesNotExist:
            await message.answer(payload.no_user_text)
    else:
        await message.answer(payload.invalid_match_text)


async def send_msg_command(message: types.Message, user: CasinoUser, match):
    try:
        await dp.bot.send_message(user.cid, match.group(2))
    except ChatNotFound:
        return
    except BotBlocked:
        return

    await message.answer(payload.casino_msg_text)


async def edit_balance(message: types.Message, user: CasinoUser, match):
    user.balance = int(match.group(2))
    user.save()
    await message.answer(f"изменил епта епта")


async def send_info_about_mamonth(message: types.Message, user: CasinoUser, match=None):
    localnow = datetime_local_now().replace(tzinfo=None)
    timenow = localnow.strftime("%H:%M, %S cек")

    await message.answer(
        payload.casino_mamonth_info.format(
            smile=random_heart(),
            uid=user.id,
            chat_id=user.cid,
            name=user.fullname,
            balance=user.balance,
            fortune="Вкл"
            if user.fort_chance == 100
            else "Выкл"
            if user.fort_chance == 0
            else f"{user.fort_chance} %",
            time=timenow,
        ),
        reply_markup=cas_info_keyboard(user.fort_chance, user.id, "PIZDA"),
    )


@dp.message_handler(commands="msg", state=Casino.commands, is_worker=True)
async def cas_mamonth_msg(message: types.Message):
    await match_command(message, r"\/msg (c\d+|\d+);(.+)", send_msg_command)


@dp.message_handler(commands="bal", state=Casino.commands, is_worker=True)
async def cas_mamonth_bal(message: types.Message):
    await match_command(message, r"\/bal (c\d+|\d+);(\d+)", edit_balance)


@dp.message_handler(commands="info", state=Casino.commands, is_worker=True)
async def cas_mamonth_info(message: types.Message):
    await match_command(message, r"\/info (c\d+|\d+)", send_info_about_mamonth)


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "updatefart",
    state="*",
    is_worker=True,
)
async def update_mamonth_fart(query: types.CallbackQuery):
    try:
        user = CasinoUser.get(id=query.data.split("_")[1])  # can get by str
        user.fort_chance = int(
            100 if user.fort_chance == 0 else 50 if user.fort_chance == 100 else 0
        )

        user.save()

        localnow = datetime_local_now().replace(tzinfo=None)
        timenow = localnow.strftime("%H:%M, %S cек")

        await query.message.edit_text(
            payload.casino_mamonth_info.format(
                smile=random_heart(),
                uid=user.id,
                chat_id=user.cid,
                name=user.fullname,
                fortune="Вкл"
                if user.fort_chance == 100
                else "Выкл"
                if user.fort_chance == 0
                else f"{user.fort_chance} %",
                username=user.username,
                balance=user.balance,
                time=timenow,
            ),
            reply_markup=cas_info_keyboard(user.fort_chance, user.id, "PIZDA"),
        )
    except CasinoUser.DoesNotExist:
        logger.debug("Mamonth that worker want see does not exist.")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "casupdateinfo",
    is_worker=True,
)
async def update_mamonth_info(query: types.CallbackQuery):
    try:
        user = CasinoUser.get(id=query.data.split("_")[1])  # can get by str

        localnow = datetime_local_now().replace(tzinfo=None)
        timenow = localnow.strftime("%H:%M, %S cек")

        await query.message.edit_text(
            payload.casino_mamonth_info.format(
                smile=random_heart(),
                uid=user.id,
                chat_id=user.cid,
                name=user.fullname,
                fortune="Вкл"
                if user.fort_chance == 100
                else "Выкл"
                if user.fort_chance == 0
                else f"{user.fort_chance} %",
                username=user.username,
                balance=user.balance,
                time=timenow,
            ),
            reply_markup=cas_info_keyboard(user.fort_chance, user.id, "PIZDA"),
        )
    except CasinoUser.DoesNotExist:
        logger.debug("Mamonth that worker want see does not exist.")


async def change_fart_mamonth(message: types.Message, user: CasinoUser, match):
    user.fort_chance = (
        100 if user.fort_chance == 0 else 50 if user.fort_chance == 100 else 0
    )
    user.save()

    if user.fort_chance == 0:
        await message.answer(
            payload.fart_off_text.format(
                name=user.fullname,
            )
        )
    elif user.fort_chance == 50:
        await message.answer(
            payload.fart_fif_text.format(
                name=user.fullname,
            )
        )
    else:
        await message.answer(
            payload.fart_on_text.format(
                name=user.fullname,
            )
        )


@dp.message_handler(commands="fart", state=Casino.commands, is_worker=True)
async def cas_fart_command(message: types.Message):
    await match_command(message, r"\/fart (c\d+|\d+)", change_fart_mamonth)


async def delete_mamonth(message: types.Message, user: CasinoUser, match):
    logger.debug(f"Deleting Casino UserId {user.id} CasinoHistory")
    CasinoUserHistory.delete().where(
        CasinoUserHistory.owner == user
    ).execute()  # delete all history
    logger.debug(f"Deleting Casino UserId {user.id} CasinoPayment")
    CasinoPayment.delete().where(
        CasinoPayment.owner == user
    ).execute()  # delete all payments
    logger.debug(f"Deleting Casino UserId {user.id} Instance")
    user.delete_instance()  # delete user instance
    await message.answer(payload.mamonth_delete_text.format(name=user.fullname))


@dp.message_handler(commands="del", state=Casino.commands, is_worker=True)
async def cas_fart_command(message: types.Message):
    await match_command(message, r"\/del (c\d+|\d+)", delete_mamonth)


def small_mamont(user: CasinoUser) -> str:
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


@dp.callback_query_handler(text="my_mamonths", state=Casino.commands, is_worker=True)
async def cas_mamonths_info(query: types.CallbackQuery):
    worker = Worker.get(cid=query.from_user.id)
    mamonths_count = worker.cas_users.count()
    localnow = datetime_local_now().replace(tzinfo=None)
    timenow = localnow.strftime("%H:%M, %S cек")

    if mamonths_count == 0:
        await query.answer("Вывожу!")
        await query.message.answer(payload.no_mamonths_text)
    else:
        mamonths_text = "\n".join(map(small_mamont, worker.cas_users))
        await query.message.answer(
            payload.all_mamonths_text.format(
                mamonths_count=mamonths_count,
                all_mamonths=mamonths_text,
                time=timenow,
            )
        )


@dp.callback_query_handler(text="my_frazes", state=Casino.commands, is_worker=True)
async def cas_mamonths_phrazes(query: types.CallbackQuery):
    await query.answer("Работаю хули")


@dp.callback_query_handler(text="my_promos", state=Casino.commands, is_worker=True)
async def cas_mamonths_promos(query: types.CallbackQuery):
    await query.answer("Работаю")


@dp.callback_query_handler(text="my_all_alerts", state=Casino.commands, is_worker=True)
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
            except (ChatNotFound, BotBlocked):
                continue

            await query.message.edit_text(
                payload.cas_alsend_text.format(
                    text=data["text"], msg_count=msg_count, msg_len=msg_len
                )
            )
    await state.finish()


@dp.callback_query_handler(text="my_delete_all", state=Casino.commands, is_worker=True)
async def cas_mamonths_delete(query: types.CallbackQuery):
    await query.answer("Работаю")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "payaccept", is_worker=True
)
async def accept_pay(query: types.CallbackQuery):
    pay_id = query.data.split("_")[1]
    try:
        pay = CasinoPayment.get(id=pay_id)
        pay.done = True
        pay.save()
        await query.message.edit_text(
            query.message.parse_entities() + "\n\nВы пополнили баланс"
        )
        await query.answer("Принял")
    except CasinoPayment.DoesNotExist:
        await query.answer("Ошибка!")
