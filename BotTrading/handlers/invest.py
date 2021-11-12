from aiogram import types

from loader import currency_worker
from models import TradingUser
from data import texts
from data.states import Bet
from data.keyboards import invest_keyboard, bet_keyboard, choice_fix_keyboard


async def invest_handler(message: types.Message):
    active_infos = "\n".join(
        map(
            lambda curr: texts.active_info.format(
                name=curr["name"],
                price_usd=curr["price_usd"],
                price_rub=curr["price"],
            ),
            currency_worker.currencies,
        )
    )
    await message.answer(
        texts.invest.format(
            active_infos=active_infos,
        ),
        reply_markup=invest_keyboard(
            list(map(lambda c: c["keyboard_name"], currency_worker.currencies))
        ),
    )


async def get_currency_info(query: types.CallbackQuery):
    curr_id = int(query.data.split("_")[1])
    currency = currency_worker.get_currency(curr_id)
    await query.message.edit_text(
        texts.currency_info.format(
            currency_name=currency["name"],
            symbol=currency["symbol"],
            price_usd=currency["price_usd"],
            price_rub=currency["price"],
            description=currency["description"],
        ),
        reply_markup=bet_keyboard(curr_id),
    )


async def bet_handler(query: types.CallbackQuery, user: TradingUser):
    curr_id = int(query.data.split("_")[1])
    currency = currency_worker.get_currency(curr_id)
    await query.message.edit_text(
        texts.bet_amount_insert.format(
            currency_name=currency["name"], amount=user.balance
        )
    )
    await Bet.amount.set()


async def non_digit_bet_amount(message: types.Message):
    await message.answer(texts.non_digit_bet_amount)


async def bet_amount(message: types.Message, user: TradingUser):
    amount = int(message.text)
    if user.balance < amount:
        await message.answer(texts.too_big_bet_amount.format(amount=user.balance))
        return
    await message.answer(texts.choice_fix_time, reply_markup=choice_fix_keyboard)
    await Bet.time.set()


async def time_selected(query: types.CallbackQuery):
    seconds = int(query.data.split("_")[1])
    await query.message.edit_text(f"chice - {seconds}")
