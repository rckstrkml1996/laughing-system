from aiogram import types
from aiogram.utils.emoji import emojize
from loguru import logger

from loader import dp, config
from data import texts
from data.keyboards import *
from models import Worker


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "reject",
    admins_chat=True,
    state="*",
    is_support=True,
)
async def summary_reject(query: types.CallbackQuery):
    try:
        worker = Worker.get(cid=query.data.split("_")[1])
        worker.send_summary = False  # can send new summary
        worker.save()
        username = f"@{worker.username} " if worker.username else " "
        await query.message.edit_text(
            texts.summary_check_text("Отклонён").format(
                name=worker.name,
                username=username,
                chat_id=worker.cid,
                where=worker.summary_info.split(";")[0],
                experience=worker.summary_info.split(";")[1],
            )
        )
        await query.answer("Отклонён!")
        await dp.bot.send_message(
            worker.cid,
            texts.summary_rejected_text,
            reply_markup=summary_start_keyboard,
        )
        logger.info(f"{query.message.chat.id} - summary denied")
    except Worker.DoesNotExist:
        logger.warning(f"{query.message.chat.id} - doen't exist")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "accept",
    admins_chat=True,
    state="*",
    is_support=True,
)
async def summary_accepted(query: types.CallbackQuery):
    try:
        worker = Worker.get(cid=query.data.split("_")[1])
        worker.status = 2  # status - worker
        worker.warns = 0
        worker.save()
        username = f"@{worker.username} " if worker.username else " "
        await query.message.edit_text(
            texts.summary_check_text("Принят").format(
                name=worker.name,
                username=username,
                chat_id=worker.cid,
                where=worker.summary_info.split(";")[0],
                experience=worker.summary_info.split(";")[1],
            )
        )
        await query.answer("Принят!")
        try:
            await dp.bot.unban_chat_member(config.workers_chat, worker.cid)
        except Exception as ex:
            logger.warning(ex)
        await dp.bot.send_message(
            worker.cid,
            texts.summary_accepted_text,
            reply_markup=summary_accepted_keyboard(
                config.outs_link,
                config.workers_link,
                config.reviews_link,
            ),
        )
        await dp.bot.send_message(
            worker.cid,
            emojize(":cold_face: :green_heart:"),
            reply_markup=menu_keyboard,
        )
        await dp.bot.send_message(
            worker.cid,
            "Можешь воспользоваться клавиатурой!",
            reply_markup=menu_keyboard,
        )
        logger.info(f"[{query.message.chat.id}] - summary accepted")
    except Worker.DoesNotExist:
        logger.warning(f"{query.message.chat.id} - doen't exist")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "block",
    admins_chat=True,
    state="*",
    is_admin=True,
)
async def summary_accepted(query: types.CallbackQuery):
    try:
        worker = Worker.get(cid=query.data.split("_")[1])
        worker.status = 1  # status - blocked
        worker.save()
        username = f"@{worker.username} " if worker.username else " "
        await query.message.edit_text(
            texts.summary_check_text("Заблокирован").format(
                name=worker.name,
                username=username,
                chat_id=worker.cid,
                where=worker.summary_info.split(";")[0],
                experience=worker.summary_info.split(";")[1],
            )
        )
        await query.answer("Заблокирован!")
        await dp.bot.send_message(
            worker.cid,
            texts.summary_blocked_text,
            reply_markup=summary_blocked_keyboard,
        )
        logger.info(f"{query.message.chat.id} - summary blocked")
    except Worker.DoesNotExist:
        logger.warning(f"{query.message.chat.id} - doen't exist")
