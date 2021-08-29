from aiogram import types
from aiogram.dispatcher import FSMContext

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
        data['where'] = message.text.replace(";", " ")

    await message.answer(payload.summary_exp_text)
    await Summary.experience.set()


@dp.message_handler(state=Summary.experience)
async def summary_final(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['exp'] = message.text.replace(";", " ")

        await message.answer(
            payload.summary_final.format(
                where=data['where'],
                experience=data['exp'],
            ),
            reply_markup=summary_send_keyboard
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
                    where=data['where'],
                    experience=data['exp'],
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
                    where=data['where'],
                    experience=data['exp'],
                ),
                reply_markup=summary_check_keyboard(query.message.chat.id),
            )
    except Worker.DoesNotExist:
        pass

    await state.finish()


@dp.callback_query_handler(lambda cb: cb.data.split('_')[0] == "reject", admins_chat=True)
async def summary_reject(query: types.CallbackQuery):
    try:
        worker = Worker.get(cid=query.data.split('_')[1])
        worker.send_summary = False  # can send new summary
        worker.save()

        username = f"@{worker.username} " if worker.username else " "

        await query.message.edit_text(
            payload.summary_check_text("Отклонён").format(
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
            payload.summary_rejected_text,
            reply_markup=summary_start_keyboard
        )
    except Worker.DoesNotExist:
        pass


@dp.callback_query_handler(lambda cb: cb.data.split('_')[0] == "accept", admins_chat=True)
async def summary_accepted(query: types.CallbackQuery):
    try:
        worker = Worker.get(cid=query.data.split('_')[1])
        worker.status = 2  # status - worker
        worker.save()

        username = f"@{worker.username} " if worker.username else " "

        await query.message.edit_text(
            payload.summary_check_text("Принят").format(
                name=worker.name,
                username=username,
                chat_id=worker.cid,
                where=worker.summary_info.split(";")[0],
                experience=worker.summary_info.split(";")[1],
            )
        )

        await query.answer("Принят!")
        await dp.bot.send_message(
            worker.cid,
            payload.summary_accepted_text,
            reply_markup=summary_accepted_keyboard
        )

    except Worker.DoesNotExist:
        pass


@dp.callback_query_handler(lambda cb: cb.data.split('_')[0] == "block", admins_chat=True)
async def summary_accepted(query: types.CallbackQuery):
    try:
        worker = Worker.get(cid=query.data.split('_')[1])
        worker.status = 1  # status - blocked
        worker.save()

        username = f"@{worker.username} " if worker.username else " "

        await query.message.edit_text(
            payload.summary_check_text("Заблокирован").format(
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
            payload.summary_blocked_text,
            reply_markup=summary_blocked_keyboard
        )

    except Worker.DoesNotExist:
        pass


@dp.callback_query_handler(text="fuckurself")
async def fuck_ur_self(query: types.CallbackQuery):
    await query.answer("Идем...")  # chob chlen sosali
    await query.message.edit_text(payload.summary_blockfin_text)
