from time import monotonic
from asyncio import sleep
from random import randint, uniform

from aiogram import Dispatcher, types
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher import FSMContext
from loguru import logger

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
            photo_url=currency["photo_link"],
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
    await Dispatcher.get_current().current_state().update_data(
        curr_id=curr_id, bet=int(query.data.split("_")[2])
    )  # bet - 1 - up, bet - 0 - down


async def non_digit_bet_amount(message: types.Message):
    await message.answer(texts.non_digit_bet_amount)


async def bet_amount(message: types.Message, user: TradingUser, state: FSMContext):
    amount = int(message.text)
    if user.balance < amount:
        await message.answer(texts.too_big_bet_amount.format(amount=user.balance))
        return
    await message.answer(texts.choice_fix_time, reply_markup=choice_fix_keyboard)
    await state.update_data(amount=amount)
    await Bet.time.set()


async def time_selected(
    query: types.CallbackQuery, user: TradingUser, state: FSMContext
):
    data = await state.get_data()
    win = randint(0, 99) < user.fort_chance
    currency = currency_worker.get_currency(data["curr_id"])
    seconds = int(query.data.split("_")[1])
    price_now = currency["price_usd"]
    moll = price_now * uniform(0.01, 0.02) / seconds
    go_up = (data["bet"] and win) or (not data["bet"] and not win)
    user.balance -= data["amount"]
    user.save()
    oldtime = monotonic()
    working = True
    while working:  # how many times update message!
        delta = round(monotonic() - oldtime, 2)
        if delta > seconds:
            delta = seconds
            working = False

        try:
            await query.message.edit_text(
                texts.invest_going.format(
                    invest_type=texts.up_invest_type
                    if data["bet"]
                    else texts.down_invest_type,
                    amount=data["amount"],
                    symbol=currency["symbol"],
                    price_usd=currency["price_usd"],
                    price_rub=currency["price"],
                    price_now_usd=price_now,
                    price_now_rub=price_now * currency_worker.convertion,
                    seconds=seconds,
                    seconds_reached=delta,
                )
            )
        except MessageNotModified:
            logger.info(f"{price_now=} Message not modified!")
        if go_up:
            price_now += moll
        else:
            price_now -= moll

        await sleep(3)

    if win:
        user.balance += data["amount"] * 2
        user.save()
        if data["bet"]:
            text = texts.invest_up_good.format(
                seconds=seconds,
                amount=data["amount"],
                balance=user.balance,
            )
        else:
            text = texts.invest_down_good.format(
                seconds=seconds,
                amount=data["amount"],
                balance=user.balance,
            )
    else:
        if data["bet"]:
            text = texts.invest_up_bad.format(
                seconds=seconds,
                amount=data["amount"],
                balance=user.balance,
            )
        else:
            text = texts.invest_down_bad.format(
                seconds=seconds,
                amount=data["amount"],
                balance=user.balance,
            )

    await query.message.reply(text)
