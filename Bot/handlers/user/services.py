from aiogram import types
from loguru import logger

from loader import dp, casino_bot
from models import Worker, CasinoUser, CasinoUserHistory, CasinoPayment
from data.payload import (
    fart_off_text,
    fart_fif_text,
    fart_on_text,
    mamonth_delete_text,
)
from utils.executional import get_casino_mamonth_info
from utils.filters import ServiceCommandsFilter
from utils.types import SERVICE_FIRST_LETTERS


# only info
@dp.message_handler(  # ru and en
    ServiceCommandsFilter(
        command_names=["info", "information"],
        services=SERVICE_FIRST_LETTERS,
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

                text, markup = get_casino_mamonth_info(user)
                await message.answer(text, reply_markup=markup)
            except CasinoUser.DoesNotExist:
                await message.reply("Такого мамонта не существует!")
        elif id_info[:1] == "e" or id_info[:1] == "е":
            await message.answer(id_info[1:])
        elif id_info[:1] == "t" or id_info[:1] == "т":
            await message.answer(id_info[1:])


@dp.message_handler(  # ru and en
    ServiceCommandsFilter(
        command_names=["bal", "balance"],
        services=SERVICE_FIRST_LETTERS,
        with_id=True,
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
    ServiceCommandsFilter(
        ["fart", "fort", "fortune"],
        SERVICE_FIRST_LETTERS,
    ),
    state="*",
    is_worker=True,
)
async def fart_command(message: types.Message, regexp_command):
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
    ServiceCommandsFilter(
        ["del", "delete", "del"],
        SERVICE_FIRST_LETTERS,
    ),
    state="*",
    is_worker=True,
)
async def delete_command(message: types.Message, regexp_command):
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
    ServiceCommandsFilter(
        ["msg", "message", "text"], SERVICE_FIRST_LETTERS, with_text=True
    ),
    state="*",
    is_worker=True,
)
async def message_command(message: types.Message, regexp_command):
    try:
        worker = Worker.get(cid=message.chat.id)
    except Worker.DoesNotExist:
        await message.answer("Мамонт не найден.")
        return

    id_info = regexp_command.group(1)
    text = regexp_command.group(2)
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
