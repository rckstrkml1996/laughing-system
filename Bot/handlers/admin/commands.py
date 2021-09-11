from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from customutils.models import Worker
from loguru import logger

from aiogram.utils.exceptions import ChatAdminRequired

from loader import dp
from config import config
from data import payload
from data.keyboards import *


@dp.message_handler(commands="ban", workers_chat=True, is_admin=True)
async def ban_workers_chat(message: types.Message):
    bot_user = await dp.bot.get_me()
    if message.reply_to_message:
        try:
            chat_id = message.reply_to_message.from_user.id
            if chat_id == bot_user.id:
                await message.answer("Э афигел меня кикать??")
                return
            worker = Worker.get(cid=chat_id)
            if worker.status > 4:
                await message.answer("Вы не можете забанить админа или других крутых")
                return

            worker.status = 1
            worker.save()

            try:
                kicked = await message.chat.kick(chat_id)
            except ChatAdminRequired:
                await message.answer("У бота нет прав администратора.")
                return

            if kicked:
                logger.debug(f"Banned user: {chat_id} and kicked from chat.")
                await message.reply(
                    payload.ban_success_text.format(cid=worker.cid, name=worker.name)
                )
                await dp.bot.send_message(
                    chat_id, "Вы были исключенны из бота навсегда!"
                )
            else:
                logger.debug(f"Can kick from chat user: {chat_id}")
                await message.answer("Не могу кикнуть из чата!")
        except Worker.DoesNotExist:
            await message.answer("Юзер не является пользователем бота, исключил.")
    else:
        logger.debug("/ban message reply does not exist.")


@dp.message_handler(commands="kick", workers_chat=True, is_admin=True)
async def kick_workers_chat(message: types.Message):
    bot_user = await dp.bot.get_me()
    if message.reply_to_message:
        try:
            chat_id = message.reply_to_message.from_user.id
            if chat_id == bot_user.id:
                await message.answer("Э афигел меня кикать??")
                return

            worker = Worker.get(cid=chat_id)
            if worker.status == 1:
                await message.answer("Юзер уже в бане!")
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
