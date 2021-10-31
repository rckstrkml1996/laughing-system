from aiogram import types
from aiogram.utils.exceptions import ChatAdminRequired
from loguru import logger

from models import Worker
from loader import dp
from data import texts
from data.keyboards import *


@dp.message_handler(commands="ban", workers_chat=True, is_admin=True)
async def ban_workers_chat(message: types.Message):
    bot_user = await dp.bot.get_me()
    if message.reply_to_message:
        try:
            chat_id = message.reply_to_message.from_user.id
            if chat_id == bot_user.id:
                logger.debug(f"User: {message.from_user.id} try to ban main bot!")
                await message.answer("Э афигел меня кикать??")
                return
            worker = Worker.get(cid=chat_id)
            if worker.status > 5:
                logger.debug(
                    f"User: {message.from_user.id} try to ban worker with admin status: {worker.cid}"
                )
                await message.answer("Вы не можете забанить админа или других крутых")
                return

            worker.status = 1
            worker.save()

            try:
                kicked = await message.chat.kick(chat_id)
                logger.debug(
                    f"User: {message.from_user.id} banned and kicked Worker: {chat_id}"
                )
            except ChatAdminRequired:
                logger.warning("Bot with no admin status in workers chat!")
                await message.answer("У бота нет прав администратора.")
                return

            if kicked:
                logger.debug(
                    f"User: {message.from_user.id} banned and kicked Worker: {chat_id}"
                )
                await message.reply(
                    payload.ban_success_text.format(cid=worker.cid, name=worker.name)
                )
                await dp.bot.send_message(
                    chat_id, "Вы были исключенны из бота навсегда!"
                )
            else:
                logger.info(f"Cant kick from chat user: {chat_id}")
                await message.answer("Не могу кикнуть из чата!")
        except Worker.DoesNotExist:
            await message.answer("Юзер не является пользователем бота, исключил.")
    else:
        logger.debug("/ban message with no reply")


@dp.message_handler(commands="kick", workers_chat=True, is_admin=True)
async def kick_workers_chat(message: types.Message):
    bot_user = await dp.bot.get_me()
    if message.reply_to_message:
        try:
            chat_id = message.reply_to_message.from_user.id
            if chat_id == bot_user.id:
                logger.debug(f"User: {message.from_user.id} try to ban main bot!")
                await message.answer("Э афигел меня кикать??")
                return

            worker = Worker.get(cid=chat_id)
            if worker.status >= 5:
                logger.debug(
                    f"User: {message.from_user.id} try to ban worker with admin status: {worker.cid}"
                )
                await message.answer("Вы не можете кикнуть админа или других крутых")
                return

            worker.send_summary = False
            worker.status = 0
            worker.save()

            try:
                kicked = await message.chat.kick(chat_id)
            except ChatAdminRequired:
                await message.answer("У бота нету прав администратора!")
                return

            if kicked:
                logger.debug(f"Kicked user: {chat_id} and kicked from chat.")
                await message.reply(
                    payload.kick_success_text.format(cid=worker.cid, name=worker.name)
                )
                await dp.bot.send_message(
                    chat_id,
                    "Вы были исключенны из бота, можете попробовать подать заявку!",
                    reply_markup=summary_start_keyboard,
                )
            else:
                logger.debug(f"Can kick from chat user: {chat_id}")
                await message.answer("Не могу кикнуть из чата!")
        except Worker.DoesNotExist:
            await message.answer("Юзер не является пользователем бота, исключил.")
    else:
        logger.debug("/kick message reply does not exist.")


@dp.message_handler(commands="warn", workers_chat=True, is_support=True)
async def warn_command(message: types.Message):
    if message.reply_to_message:
        chat_id = message.reply_to_message.from_user.id
        try:
            worker = Worker.get(cid=chat_id)
            if worker.status <= 2:
                worker.warns += 1
                worker.save()
                await message.reply(
                    payload.worker_warn_text.format(
                        cid=worker.cid, name=worker.name, warns=worker.warns
                    )
                )
            else:
                await message.reply("У Воркера высокий статус!")
        except Worker.DoesNotExist:
            await message.reply("Пользователь не является Воркером!")


@dp.message_handler(commands="unwarn", workers_chat=True, is_support=True)
async def warn_command(message: types.Message):
    if message.reply_to_message:
        chat_id = message.reply_to_message.from_user.id
        try:
            worker = Worker.get(cid=chat_id)
            if worker.status <= 2:
                worker.warns -= 1
                worker.save()
                await message.reply(
                    payload.worker_unwarn_text.format(
                        cid=worker.cid, name=worker.name, warns=worker.warns
                    )
                )
            else:
                await message.reply("У Воркера высокий статус!")
        except Worker.DoesNotExist:
            await message.reply("Пользователь не является Воркером!")
