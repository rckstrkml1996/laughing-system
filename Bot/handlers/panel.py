import re
from datetime import timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.input_file import InputFile
from aiogram.utils.emoji import emojize

from loader import dp
from config import StatusNames, Rates
from data import payload
from data.states import Render, Panel
from data.keyboards import *
from utils.render import *
from utils.executional import datetime_local_now
from models import Worker, Profit


@dp.callback_query_handler(text="menu", is_worker=True)
async def worker_menu(query: types.CallbackQuery):
    worker = Worker.get(cid=query.message.chat.id)
    in_team = datetime_local_now().replace(tzinfo=None) - worker.registered

    if query.message.photo:  # it cant edit when photo!
        await worker_welcome(query.message)
    else:
        worker.username = message.chat.username
        worker.save()  # update worker username
        await query.message.edit_text(
            payload.worker_menu_text.format(
                chat_id=message.chat.id,
                status=StatusNames[worker.status],
                all_balance=sum(map(lambda prft: prft.amount, worker.profits)),
                ref_balance=worker.ref_balance,
                middle_profits=0,
                len_profits=len(worker.profits),
                in_team=in_team.days,
                warns=0,
                team_status="Ворк"
            ),
            reply_markup=panel_keyboard(worker.username_hide),
        )


@dp.message_handler(regexp="hide panel")
async def worker_welcome(message: types.Message):
    try:
        worker = Worker.get(cid=message.chat.id)
        worker.username = message.chat.username
        worker.save()  # update worker username
        in_team = datetime_local_now().replace(tzinfo=None) - worker.registered

        await message.answer(emojize(":zap:"), reply_markup=menu_keyboard)
        await message.answer(
            payload.worker_menu_text.format(
                chat_id=message.chat.id,
                status=StatusNames[worker.status],
                all_balance=sum(map(lambda prft: prft.amount, worker.profits)),
                ref_balance=worker.ref_balance,
                middle_profits=0,
                len_profits=len(worker.profits),
                in_team=in_team.days,
                warns=0,
                team_status="Ворк"
            ),
            reply_markup=panel_keyboard(worker.username_hide),
        )
    except Worker.DoesNotExist:
        pass


@dp.callback_query_handler(text="profits")
async def profits(query: types.CallbackQuery):
    await query.message.edit_text(payload.profits_text, reply_markup=profits_keyboard)


@dp.callback_query_handler(text="weekprofits")
async def weekprofits(query: types.CallbackQuery):
    worker = Worker.get(cid=query.message.chat.id)
    week_ago = datetime_local_now().replace(tzinfo=None) - timedelta(days=7)
    if worker.profits:
        last_week_profits = worker.profits.select().where((week_ago <= Profit.created))
        profits = {}
        for i in range(7):
            date = datetime_local_now().replace(tzinfo=None) - timedelta(days=6-i)
            profits[date.strftime("%d.%m")] = 0
        for i in last_week_profits:
            profits[i.created.strftime("%d.%m")] += i.amount
        if not profits:
            return
        render = InputFile(render_graph(profits, query.message.chat.username))
        await query.message.delete()
        profits_len = len(last_week_profits)
        await query.message.answer_photo(
            render,
            caption=payload.week_profit_text.format(
                middle_profits=sum(profits.values()) / profits_len,
                profits_len=profits_len,
            ),
            reply_markup=backpanel_keyboard,
        )
    else:
        await query.message.edit_text(payload.week_profitinv_text, reply_markup=backpanel_keyboard)


@dp.callback_query_handler(text="rate")
async def rate(query: types.CallbackQuery):
    try:
        worker = Worker.get(cid=query.message.chat.id)

        profit, xprofit, refund = Rates[worker.rate]

        await query.message.edit_text(
            payload.rate_text.format(
                profit=profit,
                xprofit=xprofit,
                refund=refund,
            ),
            reply_markup=rate_keyboard,
        )
    except Worker.DoesNotExist:
        pass


@dp.callback_query_handler(text="changerate")
async def change_rate(query: types.CallbackQuery):
    await query.message.edit_text(
        emojize(payload.about_rates_text),
        reply_markup=changerate_keyboard
    )


@dp.callback_query_handler(lambda cb: cb.data.split('_')[0] == "cr")
async def full_change_rate(query: types.CallbackQuery):
    worker = Worker.get(cid=query.message.chat.id)
    worker.rate = query.data.split('_')[1]
    worker.save()
    await query.answer("Изменено!")
    await rate(query)


@dp.callback_query_handler(text="tools")
async def tools(query: types.CallbackQuery):
    try:
        worker = Worker.get(cid=query.message.chat.id)
        await query.message.edit_text(emojize(":hammer_and_wrench: Инструменты"),
                                      reply_markup=tools_keyboard(worker.username_hide))
    except Worker.DoesNotExist:
        pass


@dp.callback_query_handler(text="toggleusername")
async def toggle_username(query: types.CallbackQuery):
    try:
        worker = Worker.get(cid=query.message.chat.id)
        worker.username_hide = not worker.username_hide
        worker.save()
        status = "Скрыли" if worker.username_hide else "Открыли"
        await query.answer(f"Вы {status} никнейм")
    except Worker.DoesNotExist:
        pass


@dp.callback_query_handler(text="secretid")
async def secret_id(query: types.CallbackQuery):
    await query.message.edit_text(payload.change_secretid_text)
    await Panel.secret_id.set()


@dp.message_handler(state=Panel.secret_id)
async def change_secret_id(message: types.Message, state: FSMContext):
    if len(message.text) <= 8 and re.match(r"^[A-Za-z0-9]+$", message.text):
        try:
            worker = Worker.get(cid=message.chat.id)
            worker.secret_id = message.text
            worker.save()
            await message.reply(payload.new_secretid_text.format(
                secret_id=message.text
            ))
            await state.finish()
            await worker_welcome(message)
        except:
            pass
    else:
        await message.answer(payload.new_secretidinv_text)

"""
Render Start

"""


@dp.callback_query_handler(text="render")
async def render(query: types.CallbackQuery):
    await query.message.edit_text("Что будем отрисовывать?", reply_markup=render_keyboard)


@dp.callback_query_handler(text="qiwibalance")
async def render(query: types.Message):
    await query.message.edit_text(payload.render_qiwibalance_text)
    await Render.qiwibalance.set()


@dp.message_handler(state=Render.qiwibalance)
async def qiwi_balance(message: types.Message, state: FSMContext):
    text = message.text.split("\n")
    try:
        render = InputFile(render_qiwibalance(text[0], text[1]))
        await message.answer_photo(render, caption="Лови")
        await worker_welcome(message)
        await state.finish()
    except IndexError:
        pass


@dp.callback_query_handler(text="qiwitransfer")
async def render(query: types.Message):
    await query.message.edit_text(payload.render_qiwitransfer_text)
    await Render.qiwitransfer.set()


@dp.message_handler(state=Render.qiwitransfer)
async def qiwi_transfer(message: types.Message, state: FSMContext):
    text = message.text.split('\n')
    try:
        render = InputFile(render_qiwitransfer(text[0], text[1], text[2]))
        await message.answer_photo(render, caption="Лови")
        await worker_welcome(message)
        await state.finish()
    except IndexError:
        pass


@dp.callback_query_handler(text="sbertransfer")
async def render(query: types.Message):
    await query.message.edit_text(payload.render_sbertransfer_text)
    await Render.sbertransfer.set()


@dp.message_handler(state=Render.sbertransfer)
async def qiwi_transfer(message: types.Message, state: FSMContext):
    text = message.text.split('\n')
    try:
        if not re.match(r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$", text[2]):
            await message.answer("Сука неправильна ввел время\nВведи число клоун")
            return
        render = InputFile(render_sbertransfer(text[0], text[1], text[2]))
        await message.answer_photo(render, caption="Лови")
        await worker_welcome(message)
        await state.finish()
    except IndexError:
        pass
