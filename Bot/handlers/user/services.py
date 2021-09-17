from aiogram import types
from aiogram.dispatcher.filters import RegexpCommandsFilter
from loguru import logger

from customutils.models import Worker, CasinoUser, CasinoUserHistory, CasinoPayment

from loader import dp

from data.payload import fart_off_text, fart_fif_text, fart_on_text, mamonth_delete_text
from utils.executional import get_casino_mamonth_info

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
