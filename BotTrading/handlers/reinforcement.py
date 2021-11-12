from random import randint

from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from data import texts, keyboards
from data.states import Add, Out
from loader import config, main_bot
from qiwiapi import Qiwi
from qiwiapi.exceptions import InvalidProxy
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
                min_amount=config.min_deposit,
            )
        )
        return
    if isinstance(config.qiwi_tokens, list):
        qiwi = Qiwi(**config.qiwi_tokens[0])
        try:
            profile = await qiwi.get_profile()
        except InvalidProxy:
            return await message.answer("Ошибка соединения с сервером!")
        account = profile.contractInfo.contractId
        comment = randint(1000000, 9999999)
        payment = TradingPayment.create(
            owner=user,
            comment=comment,
            amount=amount,
        )
        await message.answer(
            texts.add_go.format(
                amount=amount,
                account=account,
                comment=comment,
            ),
            reply_markup=keyboards.add_keyboard(amount, account, comment, payment.id),
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
    number = message.text.replace("+", "")
    if number in list(map(lambda x: x[1:], config.fake_numbers)):
        await message.answer(
            texts.out_request.format(
                number="+" + number,
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
    elif number in list(map(lambda x: x[1:], config.fake_cards)):
        await message.answer(
            texts.out_request.format(
                number=number,
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


