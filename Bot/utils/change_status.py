from aiogram.utils.exceptions import ChatAdminRequired, BadRequest
from loguru import logger

from models import Worker
from loader import bot
from data.texts import (
    ban_success_text,
    kick_success_text,
    worker_warn_text,
    worker_unwarn_text,
    you_kicked_text,
    you_banned_text,
)
from data.keyboards import summary_start_keyboard


async def ban(chat_id: int, user_id: int):  # tg ids
    me = await bot.get_me()
    if user_id == me.id:
        await bot.send_message(chat_id, "Ты что-то попутал, да?")
        return
    try:
        worker = Worker.get(cid=user_id)
        if worker.status >= 4:
            await bot.send_message(chat_id, "У юзера высокий статус!")
            return
        worker.status = 1  # banned
        worker.save()
        # notify about kick
        await bot.send_message(
            chat_id,
            ban_success_text.format(
                cid=worker.cid,
                name=worker.name,
            ),
        )
        await bot.send_message(user_id, you_banned_text)
    except Worker.DoesNotExist:
        await bot.send_message(
            chat_id,
            ban_success_text.format(
                cid=user_id,
                name="Низнаю имени",
            ),
        )
    finally:
        try:
            await bot.kick_chat_member(chat_id, user_id)
        except ChatAdminRequired:
            logger.warning("Bot with no admin status in workers chat!")
            await bot.send_message(chat_id, "У бота нет прав администратора.")


# then try to send log that user kicked if exist in base!
async def kick(chat_id: int, user_id: int):
    me = await bot.get_me()
    if user_id == me.id:
        return
    try:
        worker = Worker.get(cid=user_id)
        if worker.status >= 4:
            await bot.send_message(chat_id, "У юзера высокий статус!")
            return
        worker.send_summary = False  # can send summary!
        worker.status = 0  # not user
        worker.save()
        # notify about kick
        await bot.send_message(
            chat_id,
            kick_success_text.format(
                cid=worker.cid,
                name=worker.name,
            ),
        )
        await bot.send_message(
            user_id, you_kicked_text, reply_markup=summary_start_keyboard
        )
    except Worker.DoesNotExist:
        await bot.send_message(
            chat_id,
            kick_success_text.format(
                cid=user_id,
                name="Низнаю имени",
            ),
        )
    finally:
        try:
            await bot.kick_chat_member(chat_id, user_id)
        except ChatAdminRequired:
            logger.warning("Bot with no admin status in workers chat!")
            await bot.send_message(chat_id, "У бота нет прав администратора.")
        except BadRequest:
            logger.error("Worker might not in chat!")


async def warn(chat_id: int, user_id: int):
    try:
        worker = Worker.get(cid=user_id)
        if worker.status <= 2:  # just worker
            worker.warns += 1
            worker.save()
            await bot.send_message(
                chat_id,
                worker_warn_text.format(
                    cid=worker.cid, name=worker.name, warns=worker.warns
                ),
            )
            if worker.warns >= 3:
                await kick(chat_id, user_id)
        else:
            await bot.send_message(chat_id, "У Воркера высокий статус!")
    except Worker.DoesNotExist:
        await bot.send_message(chat_id, "Пользователь не является Воркером в боте!")


async def unwarn(chat_id: int, user_id: int):
    try:
        worker = Worker.get(cid=user_id)
        if worker.status <= 2:  # just worker
            # if worker.warns > 0: # ahahahahaahahahahahh
            worker.warns -= 1
            worker.save()
            await bot.send_message(
                chat_id,
                worker_unwarn_text.format(
                    cid=worker.cid, name=worker.name, warns=worker.warns
                ),
            )
        else:
            await bot.send_message(chat_id, "У Воркера слишком высокий статус!")
    except Worker.DoesNotExist:
        await bot.send_message(chat_id, "Пользователь не является Воркером в боте!")
