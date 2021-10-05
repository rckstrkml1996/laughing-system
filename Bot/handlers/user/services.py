from aiogram import types
from aiogram.dispatcher.filters import RegexpCommandsFilter
from aiogram.dispatcher import FSMContext
from loguru import logger

from customutils.models import Worker, CasinoUser, CasinoUserHistory, CasinoPayment

from loader import dp, casino_bot
from config import config
from data.payload import (
    fart_off_text,
    fart_fif_text,
    fart_on_text,
    mamonth_delete_text,
    casino_text,
    trading_text,
    escort_text,
)
from data.keyboards import casino_keyboard, trading_keyboard, escort_keyboard
from utils.executional import get_casino_mamonth_info


@dp.message_handler(regexp="казин", state="*", is_worker=True)
async def casino_info(message: types.Message, worker: Worker, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logger.debug(f"Cancelling state {current_state} in bot start")
        await state.finish()

    logger.debug(f"Worker [{message.chat.id}] want get casino info")

    await message.answer(
        casino_text.format(
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
    # await Casino.commands.set()
    logger.debug(f"Worker [{message.chat.id}] get casino info succesfully")


@dp.message_handler(regexp="трейдин", is_worker=True, state="*")
async def casino_info(message: types.Message, worker: Worker):
    await message.answer(
        trading_text.format(
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
        reply_markup=trading_keyboard,
        disable_web_page_preview=True,
    )


@dp.message_handler(regexp="эскорт", is_worker=True, state="*")
async def casino_info(message: types.Message, worker: Worker):
    await message.answer(
        escort_text.format(
            worker_id=worker.uniq_key,
        ),
        reply_markup=escort_keyboard,
        disable_web_page_preview=True,
    )


# only info
@dp.message_handler(  # ru and en
    RegexpCommandsFilter(
        regexp_commands=[
            "info (c\d+|с\d+|t\d+|\d+)",
            "information (c\d+|с\d+|t\d+|\d+)",
        ]
    ),
    state="*",
    is_worker=True,
)
async def info_command(message: types.Message, regexp_command):
    try:
        worker = Worker.get(cid=message.chat.id)
    except Worker.DoesNotExist:
        return

    id_info = regexp_command.group(1)
    if id_info.isdigit():
        pass  # than telegram id
    else:  # ru and en
        if id_info[:1] == "c" or id_info[:1] == "с":
            try:
                user = CasinoUser.get(id=id_info[1:])
                if user.owner != worker:
                    logger.info(
                        f"/info Worker: {message.chat.id} try get different mamonth!"
                    )
                    return

                text, markup = await get_casino_mamonth_info(worker, user)
                await message.answer(text, reply_markup=markup)
            except CasinoUser.DoesNotExist:
                await message.reply("Такого мамонта не существует!")
        elif id_info[:1] == "e" or id_info[:1] == "е":
            await message.answer(id_info[1:])
        elif id_info[:1] == "t" or id_info[:1] == "т":
            await message.answer(id_info[1:])


@dp.message_handler(  # ru and en
    RegexpCommandsFilter(
        regexp_commands=[
            "bal (c\d+|с\d+|t\d+|\d+);(\d+)",
            "balance (c\d+|с\d+|t\d+|\d+);(\d+)",
        ]
    ),
    state="*",
    is_worker=True,
)
async def change_balance_command(message: types.Message, regexp_command):
    try:
        worker = Worker.get(cid=message.chat.id)
    except Worker.DoesNotExist:
        await message.answer("Мамонт не найден.")
        return

    amount = regexp_command.group(2)
    if not amount.isdigit():
        await message.answer("Значение для баланса должно быть числом.")
        return  # logg
    # amount = int(amount) # for peewee does not matter str or int

    id_info = regexp_command.group(1)
    if id_info.isdigit():
        pass  # than telegram id
    else:  # ru and en
        if id_info[:1] == "c" or id_info[:1] == "с":
            try:
                user = CasinoUser.get(id=id_info[1:])
                if user.owner != worker:
                    logger.info(
                        f"/bal Worker: {message.chat.id} try get different mamonth!"
                    )
                    return

                user.balance = amount
                user.save()
                await message.answer(
                    f"Изменил баланс! Новый баланс: {amount} RUB, /c{user.id}"
                )
            except CasinoUser.DoesNotExist:
                await message.reply("Такого мамонта не существует!")
        elif id_info[:1] == "t" or id_info[:1] == "т":
            await message.answer(id_info[1:])


@dp.message_handler(  # ru and en
    RegexpCommandsFilter(
        regexp_commands=[
            "fart (c\d+|с\d+|t\d+|\d+)",
            "fort (c\d+|с\d+|t\d+|\d+)",
        ]
    ),
    state="*",
    is_worker=True,
)
async def change_balance_command(message: types.Message, regexp_command):
    try:
        worker = Worker.get(cid=message.chat.id)
    except Worker.DoesNotExist:
        await message.answer("Мамонт не найден.")
        return

    id_info = regexp_command.group(1)
    if id_info.isdigit():
        pass  # than telegram id
    else:  # ru and en
        if id_info[:1] == "c" or id_info[:1] == "с":
            try:
                user = CasinoUser.get(id=id_info[1:])
                if user.owner != worker:
                    logger.info(
                        f"/bal Worker: {message.chat.id} try get different mamonth!"
                    )
                    return

                user.fort_chance = (
                    100
                    if user.fort_chance == 0
                    else 50
                    if user.fort_chance == 100
                    else 0
                )
                user.save()

                if user.fort_chance == 0:
                    await message.answer(
                        fart_off_text.format(
                            name=user.fullname,
                        )
                    )
                elif user.fort_chance == 50:
                    await message.answer(
                        fart_fif_text.format(
                            name=user.fullname,
                        )
                    )
                else:
                    await message.answer(
                        fart_on_text.format(
                            name=user.fullname,
                        )
                    )
            except CasinoUser.DoesNotExist:
                await message.reply("Такого мамонта не существует!")
        elif id_info[:1] == "t" or id_info[:1] == "т":
            await message.answer(id_info[1:])


@dp.message_handler(  # ru and en
    RegexpCommandsFilter(
        regexp_commands=[
            "del (c\d+|с\d+|t\d+|e\d+|\d+)",
            "delete (c\d+|с\d+|t\d+|e\d+|\d+)",
        ]
    ),
    state="*",
    is_worker=True,
)
async def change_balance_command(message: types.Message, regexp_command):
    try:
        worker = Worker.get(cid=message.chat.id)
    except Worker.DoesNotExist:
        await message.answer("Мамонт не найден.")
        return

    id_info = regexp_command.group(1)
    if id_info.isdigit():
        pass  # than telegram id
    else:  # ru and en
        if id_info[:1] == "c" or id_info[:1] == "с":
            try:
                user = CasinoUser.get(id=id_info[1:])
                if user.owner != worker:
                    logger.info(
                        f"/bal Worker: {message.chat.id} try get different mamonth!"
                    )
                    return

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
                await message.answer(mamonth_delete_text.format(name=user.fullname))
                logger.debug("Mamonths deleted.")
            except CasinoUser.DoesNotExist:
                await message.reply("Такого мамонта не существует!")
        elif id_info[:1] == "t" or id_info[:1] == "т":
            await message.answer(id_info[1:])


@dp.message_handler(  # ru and en
    fullregexp_commands=[
        "msg (c\d+|с\d+|t\d+|e\d+|\d+);(.+)",
        "message (c\d+|с\d+|t\d+|e\d+|\d+);(.+)",
    ],
    state="*",
    is_worker=True,
)
async def change_balance_command(message: types.Message, full_regexp):
    try:
        worker = Worker.get(cid=message.chat.id)
    except Worker.DoesNotExist:
        await message.answer("Мамонт не найден.")
        return

    id_info = full_regexp.group(1)
    text = full_regexp.group(2)
    if id_info.isdigit():
        pass  # than telegram id
    else:  # ru and en
        if id_info[:1] == "c" or id_info[:1] == "с":
            try:
                user = CasinoUser.get(id=id_info[1:])
                if user.owner != worker:
                    logger.info(
                        f"/msg Worker: {message.chat.id} try get different mamonth!"
                    )
                    return

                try:
                    await casino_bot.send_message(user.cid, text)
                    await message.answer(
                        f"Успешно отправил сообщение мамонту /c{user.id}"
                    )
                except Exception as e:
                    await message.answer("Не отправилось :(")
                    logger.exception(e)
            except CasinoUser.DoesNotExist:
                await message.reply("Такого мамонта не существует!")
        elif id_info[:1] == "t" or id_info[:1] == "т":
            await message.answer(id_info[1:])
