import asyncio
from aiogram import types
from customutils.models import Worker
from data.config import config, photos
from data.states import Asset
import asyncio
from data import payload
from data.keyboards import *
from loader import dp
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text="btc")
async def btc_choosed(query: types.CallbackQuery):
    await query.message.answer_photo(photos["btc"], 
                                    payload.bitcoin_info_text,
                                    reply_markup=investing_keyboard)

@dp.callback_query_handler(text="eth")
async def btc_choosed(query: types.CallbackQuery):
    await query.message.answer_photo(photos["eth"],
                                    payload.eth_info_text,
                                    reply_markup=investing_keyboard)

@dp.callback_query_handler(text="trx")
async def btc_choosed(query: types.CallbackQuery):
    await query.message.answer_photo(photos["trx"],
                                payload.trx_info_text,
                                reply_markup=investing_keyboard)

@dp.callback_query_handler(text="ltc")
async def btc_choosed(query: types.CallbackQuery):
    await query.message.answer_photo(photos["ltc"],
                                    payload.ltc_info_text,
                                    reply_markup=investing_keyboard)

@dp.callback_query_handler(text="xrp")
async def btc_choosed(query: types.CallbackQuery):
    await query.message.answer_photo(photos["xrp"],
                                    payload.xrp_info_text,
                                    reply_markup=investing_keyboard)

@dp.callback_query_handler(text="qtm")
async def btc_choosed(query: types.CallbackQuery):
    await query.message.answer_photo(photos["qtm"],
                                payload.qtum_info_text, 
                                reply_markup=investing_keyboard)

@dp.callback_query_handler(text="count")
async def bet_count(query: types.CallbackQuery):
    try:
        worker = Worker.get(cid=query.message.chat.id)
        await query.message.answer(payload.ecn_selected_text.format(
            balance=worker.ref_balance
        ))
        await Asset.count.set()
    except Worker.DoesNotExist:
        pass

@dp.message_handler(state=Asset.count)
async def requisites_entered(message: types.Message, state: FSMContext):
    try:
        worker = Worker.get(cid=message.chat.id)
        try:
            bet_count = int(message.text)
            if bet_count <= worker.ref_balance and bet_count >= config("min_deposit"):
                async with state.proxy() as data:
                    data['bet_count'] = message.text.replace(" ", ";")
                    await message.answer(payload.ecn_bet_start.format(
                        bet_timer = config("bet_timer")
                    ))
                    await asyncio.sleep(config("bet_timer"))
                    worker.ref_balance += int(data['bet_count'])
                    worker.save()
                    await message.answer(payload.ecn_bet_win.format(
                                        win_count=int(data['bet_count']),
                                        balance=worker.ref_balance
                    ), reply_markup=investing_keyboard)
                    await state.finish()
            else:
                await message.answer(payload.not_enough_balance_text)
        except ValueError:
            await message.answer(payload.int_error_text)
    except Worker.DoesNotExist:
        pass