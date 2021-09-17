from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from loader import dp
from data.states import Summary
from data import payload
from config import config  # ADMINS_CHAT
from data.keyboards import *
from customutils.models import Worker


async def new_request(message: types.Message):
    await message.answer(payload.new_summary_text, reply_markup=summary_start_keyboard)


@dp.callback_query_handler(text="summary", send_summary=False)
async def summary_main(query: types.CallbackQuery):
    await summary_rules(query.message)


async def summary_rules(message: types.Message):
    await message.edit_text(payload.rules_text(), reply_markup=summary_rules_keyboard)


@dp.callback_query_handler(text="agreesummary", send_summary=False)
async def summary_agree(query: types.CallbackQuery):
    await query.message.edit_text(payload.rules_text(True))
    await query.message.answer(payload.summary_where_text)
    await Summary.where.set()


@dp.message_handler(state=Summary.where)
async def summary_experience(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["where"] = message.text.replace(";", " ")

    await message.answer(payload.summary_exp_text)
    await Summary.experience.set()


@dp.message_handler(state=Summary.experience)
async def summary_final(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["exp"] = message.text.replace(";", " ")

        await message.answer(
            payload.summary_final.format(
                where=data["where"],
                experience=data["exp"],
            ),
            reply_markup=summary_send_keyboard,
        )

    await Summary.final.set()


@dp.callback_query_handler(state=Summary.final, text="sendsummary")
async def summary_send(query: types.CallbackQuery, state: FSMContext):
    try:
        worker = Worker.get(cid=query.message.chat.id)
        worker.send_summary = True  # cant send new summary

        async with state.proxy() as data:
            await query.message.edit_text(  # message to user
                payload.summary_sended_text.format(
                    where=data["where"],
                    experience=data["exp"],
                )
            )

            worker.summary_info = f"{data['where']};{data['exp']}"
            worker.save()

            username = f"@{worker.username} " if worker.username else " "

            await dp.bot.send_message(  # message to admins chat
                config("admins_chat"),
                payload.summary_check_text().format(
                    name=query.message.chat.full_name,
                    username=username,
                    chat_id=query.message.chat.id,
                    where=data["where"],
                    experience=data["exp"],
                ),
                reply_markup=summary_check_keyboard(query.message.chat.id),
            )
            logger.debug(f"{query.message.chat.id} send a summary")
    except Worker.DoesNotExist:
        logger.debug(f"{query.message.chat.id} - doen't exist")

    await state.finish()


@dp.callback_query_handler(text="fuckurself")
async def fuck_ur_self(query: types.CallbackQuery):
    await query.answer("Идем...")  # chob chlen sosali
    await query.message.edit_text(payload.summary_blockfin_text)
