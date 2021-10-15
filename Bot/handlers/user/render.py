from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.emoji import emojize
from aiogram.types.input_file import InputFile
from loguru import logger

from loader import dp
from data.states import Render
from data.payload import (
    render_main_text,
    render_qiwi_balance_text,
    render_qiwi_trans_text,
    render_sber_trans_text,
)
from data.keyboards import render_main_keyboard, to_menu_keyboard
from utils.render import render_sbertransfer, render_qiwitransfer, render_qiwibalance


@dp.callback_query_handler(text="render")
async def render_main(query: types.CallbackQuery):
    await query.message.delete()  # delete than answer) im 15 years old)
    await query.message.answer(
        render_main_text,
        reply_markup=render_main_keyboard,
    )


@dp.callback_query_handler(text="render_qiwibalance", is_worker=True, state="*")
async def render_qiwi_balance(query: types.CallbackQuery):
    await query.message.edit_text(
        render_qiwi_balance_text, reply_markup=to_menu_keyboard
    )
    await Render.qiwi_balance.set()


@dp.message_handler(state=Render.qiwi_balance)
async def render_qiwi_balance_done(message: types.Message, state: FSMContext):
    await message.answer(emojize(":cold_face::receipt:"))

    render_val = message.text.split("\n")
    logger.debug(f"Rendering Qiwi Balance {render_val=}")

    if len(render_val) >= 2:
        render = InputFile(render_qiwibalance(render_val[0], render_val[1]))
        await state.finish()
        await message.answer_photo(
            render, caption=emojize("Вот твой балансик) :snake:")
        )
    else:
        await message.answer(render_qiwi_balance_text, reply_markup=to_menu_keyboard)


@dp.callback_query_handler(text="render_qiwitrans", is_worker=True, state="*")
async def render_qiwi_balance(query: types.CallbackQuery):
    await query.message.edit_text(render_qiwi_trans_text, reply_markup=to_menu_keyboard)
    await Render.qiwi_trans.set()


@dp.message_handler(state=Render.qiwi_trans)
async def render_qiwi_trans_done(message: types.Message, state: FSMContext):
    await message.answer(emojize(":cold_face::receipt:"))
    render_val = message.text.split("\n")
    logger.debug(f"Rendering Qiwi Transaction {render_val=}")

    if len(render_val) >= 3:
        render = InputFile(
            render_qiwitransfer(render_val[0], render_val[1], render_val[2])
        )
        await state.finish()
        await message.answer_photo(
            render, caption=emojize("Вот твоя отрисовочка) :snake:")
        )
    else:
        await message.answer(render_qiwi_trans_text, reply_markup=to_menu_keyboard)


@dp.callback_query_handler(text="render_sbertrans", is_worker=True, state="*")
async def render_qiwi_balance(query: types.CallbackQuery):
    await query.message.edit_text(render_sber_trans_text, reply_markup=to_menu_keyboard)
    await Render.sber_trans.set()


@dp.message_handler(state=Render.sber_trans)
async def render_sber_trans_done(message: types.Message, state: FSMContext):
    await message.answer(emojize(":cold_face::receipt:"))
    render_val = message.text.split("\n")
    logger.debug(f"Rendering Sber Transaction {render_val=}")

    if len(render_val) >= 3:
        render = InputFile(
            render_sbertransfer(render_val[0], render_val[1], render_val[2])
        )
        await state.finish()
        await message.answer_photo(render, caption=emojize("Сбер нахуй :snake:"))
    else:
        await message.answer(render_sber_trans_text, reply_markup=to_menu_keyboard)
