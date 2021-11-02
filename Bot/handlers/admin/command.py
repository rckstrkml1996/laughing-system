from aiogram.types import Message

from loader import dp
from data.keyboards import *
from utils import change_status


@dp.message_handler(commands="ban", workers_chat=True, is_admin=True)
async def ban_workers_chat(message: Message):
    if message.reply_to_message:
        await change_status.ban(message.chat.id, message.reply_to_message.from_user.id)


@dp.message_handler(commands="kick", workers_chat=True, is_admin=True)
async def kick_workers_chat(message: Message):
    if message.reply_to_message:
        await change_status.kick(message.chat.id, message.reply_to_message.from_user.id)


@dp.message_handler(commands="warn", workers_chat=True, is_support=True)
async def warn_command(message: Message):
    if message.reply_to_message:
        await change_status.warn(message.chat.id, message.reply_to_message.from_user.id)


@dp.message_handler(commands="unwarn", workers_chat=True, is_support=True)
async def warn_command(message: Message):
    if message.reply_to_message:
        await change_status.unwarn(message.chat.id, message.reply_to_message.from_user.id)
