import random
import re

from aiogram import types
from customutils.models import CasinoUser, Worker
from customutils.datefunc import datetime_local_now

from config import config
from loader import dp
from data import payload
from data.states import Casino
from data.keyboards import *
from utils.executional import random_heart


@dp.message_handler(regexp="казин")
async def casino_info(message: types.Message):
    try:
        worker = Worker.get(cid=message.chat.id)
        await message.answer(
            payload.casino_text.format(
                worker_id=worker.uniq_key,
                pay_cards="\n".join(
                    map(
                        lambda c: f'&#127479;&#127482; {c[1:]}' if c[0] == "r" else f'&#127482;&#127462; {c[1:]}', config(
                            "fake_cards")
                    )
                ),
                pay_qiwis="\n".join(
                    map(
                        lambda c: f'&#127479;&#127482; {c[1:]}' if c[0] == "r" else f'&#127482;&#127462; {c[1:]}', config(
                            "fake_numbers")
                    )
                ),
            ),
            reply_markup=casino_keyboard,
            disable_web_page_preview=True
        )
        await Casino.commands.set()
    except Worker.DoesNotExist:
        pass  # logging


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
                await message.answer("у тебя нету такова мамонта")
        except CasinoUser.DoesNotExist:
            await message.answer("нет такого юзера")
    else:
        await message.answer("неправильно ввел епта")


async def send_msg_command(message: types.Message, user: CasinoUser, match):
    await dp.bot.send_message(user.cid, match.group(2))
    await message.answer(f"отправил епта")


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
            username=user.username,
            balance=user.balance,
            time=timenow,
        ), reply_markup=cas_info_update_keyboard(user.id)
    )


@dp.message_handler(commands="msg", state=Casino.commands)
async def cas_mamonth_msg(message: types.Message):
    await match_command(message, r"\/msg (c\d+|\d+);(.+)", send_msg_command)


@dp.message_handler(commands="bal", state=Casino.commands)
async def cas_mamonth_bal(message: types.Message):
    await match_command(message, r"\/bal (c\d+|\d+);(\d+)", edit_balance)


@dp.message_handler(commands="info", state=Casino.commands)
async def cas_mamonth_info(message: types.Message):
    await match_command(message, r"\/info (c\d+|\d+)", send_info_about_mamonth)


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "updateinfo", state=Casino.commands)
async def update_mamonth_info(query: types.CallbackQuery):
    localnow = datetime_local_now().replace(tzinfo=None)
    timenow = localnow.strftime("%H:%M, %S cек")

    await query.message.edit_text(
        payload.casino_mamonth_info.format(
            smile=random_heart(),
            uid=user.id,
            chat_id=user.cid,
            name=user.fullname,
            username=user.username,
            balance=user.balance,
            time=timenow,
        ), reply_markup=cas_info_update_keyboard(user.id)
    )
