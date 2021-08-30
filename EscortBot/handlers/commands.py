from aiogram import types

from customutils.models import EscortUser

from loader import dp
from data import payload
from loguru import logger


@dp.message_handler(commands=["info"], state="*")
async def info(message: types.Message):
    user_id = message.get_args()
    try:
        user = EscortUser.get(cid=user_id)
        await message.answer(payload.info_user_text(user.cid, user.balance))
    except EscortUser.DoesNotExist:
        logger.warning(f"{user.cid} doesn't exist")

@dp.message_handler(commands=["del"], state="*")
async def delete_mamonth(message: types.Message):
    user_id = message.get_args()
    try:
        user = EscortUser.get(cid=user_id)
        user.delete_instance()
        await message.answer(payload.mamonth_delete_text.format(name=user.fullname))
    except EscortUser.DoesNotExist:
        logger.warning(f"{user.cid} doesn't exist")


@dp.message_handler(commands=["mgs"], state="*")
async def delete_mamonth(message: types.Message):
    args = message.get_args()(";")
    cid = args[0]
    message_text = args[1]
    try:
        user = EscortUser.get(cid=cid)
        await message.answer(payload.mamonth_msg_text)
        await message.answer(cid, message_text)
        logger.warning(f"Message sent to [{user.cid}]")
    except EscortUser.DoesNotExist:
        logger.warning(f"{user.cid} doesn't exist")
    
    