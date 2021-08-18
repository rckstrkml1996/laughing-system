from loader import dp  # , qiwis
from data.states import SelfCabine, AddBalance, OutBalance
import random

from aiogram import types
from aiogram.types import ChatType
from aiogram.dispatcher.filters.builtin import Text
from aiogram.utils.markdown import quote_html
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound
from aiogram.utils.emoji import emojize
from customutils.models import CasinoUser, CasinoUserHistory
from loguru import logger

import keyboards
from data import payload
# from config import FAKE_NUMBER, OUT_CHAT, WORKERS_CHAT, PROMOS, MINIK
PROMOS = {}
FAKE_NUMBER = "666666666"
WORKERS_CHAT = "None"
OUT_CHAT = "None"
MINIK = 122

"""
Пополнение, вывод - тут
"""


@dp.message_handler(Text(startswith="пополн", ignore_case=True),
                    chat_type=ChatType.PRIVATE, state="*")
async def add_in_game(message: types.Message):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(payload.add_text)
        await AddBalance.amount.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"#{message.chat.id} - does not exist")


@dp.message_handler(lambda mes: not mes.text.isdigit(),
                    chat_type=ChatType.PRIVATE, state=AddBalance.amount)
async def add_reqiz_invalid(message: types.Message):
    await message.reply("Сумма должна быть числом.\n\nВведите сумму пополнения")


@dp.message_handler(chat_type=ChatType.PRIVATE, state=AddBalance.amount)
async def add_reqiz(message: types.Message, state: FSMContext):
    amount = int(message.text)
    if amount < MINIK:
        await message.answer(f"Минимальная сумма депозита - <b>{MINIK} RUB</b>")
        return
    try:
        user = CasinoUser.get(cid=message.chat.id)
        async with state.proxy() as data:
            data["amount"] = amount
        comment = random.randint(1000000, 9999999)
        # number = random.choice(list(qiwis.keys()))
        number = "777777777"
        # Payment.create(cid=message.chat.id, comment=comment, amount=amount)
        # await message.answer(payload.add_req_text(amount, comment, number),
        #                      reply_markup=keyboards.add_req_keyboard(amount, comment, number))
        username = "Нету"
        if message.chat.username:
            username = "@" + message.chat.username
        refer = CasinoUser.get(cid=user.refer)
        if refer.worker == True:
            await dp.bot.send_message(refer.cid, f"Заявка на пополнение \
				\nСумма: <b>{message.text}</b> RUB \
				\nМамонт: <b>{quote_html(message.chat.full_name)}</b> \
				\n{username} id: <b>{user.cid}</b>",
                                      reply_markup=keyboards.payment_done_keyboard(user.cid, comment))
    except CasinoUser.DoesNotExist:
        logger.debug(f"#{message.chat.id} - does not exist")
    finally:
        await SelfCabine.main.set()


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "done",
                           chat_type=ChatType.PRIVATE, state="*")
async def add_done(query: types.CallbackQuery):
    pass
    # try:
    #     # user_payment = Payment.get(cid=query.data.split(
    #     #     "_")[1], comment=query.data.split("_")[2])
    #     user_payment.done = True
    #     user_payment.save()
    #     await query.message.edit_text(quote_html(query.message.text) +
    #                                   emojize("\n:white_check_mark: Статус платежа - ОПЛАЧЕНО"))
    # except Payment.DoesNotExist:
    #     logger.warning(
    #         f"for #{query.message.chat.id} - payment does not exist")
    #     await query.message.answer("Ошибка! :(")


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "check",
                           chat_type=ChatType.PRIVATE, state="*")
async def add_check(query: types.CallbackQuery):
    return
    # try:
    #     user = CasinoUser.get(cid=query.message.chat.id)
    #     comment = query.data.split("_")[1]
    #     number = query.data.split("_")[2]
    #     try:
    #         # user_payment = Payment.get(
    #         #     cid=query.message.chat.id, comment=comment)

    #         if user_payment.done:
    #             await query.message.delete()
    #             user_payment.delete_instance()
    #             user.balance += user_payment.amount
    #             user.balance += user.bonus
    #             user.premium = True
    #             CasinoUserHistory.create(cid=query.message.chat.id, editor=4,
    #                                      amount=user_payment.amount, balance=user.balance)
    #             await query.message.answer(payload.add_succesful(user_payment.amount + user.bonus))
    #             user.bonus = 0
    #             user.save()
    #             return

    #         # payments = await qiwis[number].last_recharges(30)
    #         payments = []
    #         for payment in payments:
    #             if payment['sum']['amount'] >= user_payment.amount and payment['sum']['currency'] == 643:
    #                 if payment['comment'] == comment:
    #                     await query.message.delete()
    #                     user_payment.delete_instance()
    #                     # shit
    #                     from .admin_panel import PAYMENTS_MODE

    #                     if OUT_CHAT:
    #                         try:
    #                             username = query.message.chat.username
    #                             if username is None:
    #                                 mamonth = "Нет юзернейма"
    #                             else:
    #                                 username_p1 = username[:int(
    #                                     len(username) / 2 - 1)]
    #                                 username_p2 = username[int(
    #                                     len(username) / 2 + 1):]
    #                                 mamonth = "@" + username_p1 + "**" + username_p2

    #                             refer = CasinoUser.get(cid=user.refer)
    #                             if user_payment.amount < 500:
    #                                 user.fuckedup = False
    #                             share = refer.share - 25 if user.fuckedup else refer.share
    #                             worker_amount = int(
    #                                 share / 100 * user_payment.amount)
    #                             status = "<b>ТП</b>" if user.fuckedup else "<b>Залёт</b>"
    #                             out_text = emojize(f":pick: <i>Казино тип</i> - {status} \
    # 								\n:pizza: Доля воркера: <b>{worker_amount} RUB</b> (-{100 - share}%)\
    # 								\n:credit_card: Сумма: <b>{user_payment.amount} RUB</b> \
    # 								\n:cherry_blossom: Воркер: <b>{refer.username}</b>")
    #                             await dp.bot.send_message(OUT_CHAT, out_text)
    #                             await dp.bot.send_message(WORKERS_CHAT, out_text)
    #                             if refer.worker:
    #                                 await dp.bot.send_message(refer.cid, f"Мамонт пополнил {user_payment.amount} RUB \
    # 									\nМамонт: @{username} {query.message.chat.full_name} \
    # 									\n[<code>{user.cid}</code>]")
    #                         except CasinoUser.DoesNotExist:
    #                             logger.warning(
    #                                 f"#{user.refer} - does not exist")
    #                     if PAYMENTS_MODE:
    #                         user.balance += user_payment.amount
    #                         user.balance += user.bonus
    #                         CasinoUserHistory.create(cid=query.message.chat.id,
    #                                                  amount=user_payment.amount, balance=user.balance)
    #                         enroll_refer_share(user_payment.amount, user.refer)

    #                         await query.message.answer(payload.add_succesful(user_payment.amount + user.bonus))
    #                         user.fuckedup = True  # cлед пополнение -25%
    #                         user.bonus = 0
    #                         user.save()
    #                         return
    #     except Payment.DoesNotExist:
    #         logger.warning(
    #             f"for #{query.message.chat.id} - payment does not exist")
    #         await query.message.answer("Похоже вы уже оплатили этот счёт или он не существует.")
    #         return
    #     await query.message.answer(payload.add_unsuccesful)
    # except CasinoUser.DoesNotExist:
    #     logger.debug(f"#{query.message.chat.id} - does not exist")


@dp.message_handler(Text(startswith="выв", ignore_case=True), chat_type=ChatType.PRIVATE, state="*")
async def out_game(message: types.Message):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(emojize(f"Введите сумму вывода :money_with_wings: \
			\nВаш баланс: <b>{user.balance} RUB</b>"),
                             reply_markup=keyboards.cancel_keyboard)
        await OutBalance.amount.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"#{message.chat.id} - does not exist")


@dp.message_handler(lambda mes: not mes.text.isdigit() or mes.text == "0",
                    chat_type=ChatType.PRIVATE, state=OutBalance.amount)
async def out_amount_invalid(message: types.Message):
    await message.reply(quote_html("Вы ввели некорректную сумму вывода!"))


@dp.message_handler(chat_type=ChatType.PRIVATE, state=OutBalance.amount)
async def out_amount(message: types.Message, state: FSMContext):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        if user.balance >= int(message.text):
            async with state.proxy() as data:
                data['amount'] = int(message.text)
            await message.answer(payload.out_req_text)
            await OutBalance.number.set()
        elif user.balance < int(message.text):
            await message.answer("Недостаточно средств для вывода",
                                 reply_markup=keyboards.cancel_keyboard)
    except CasinoUser.DoesNotExist:
        logger.debug(f"#{message.chat.id} - does not exist")


@dp.message_handler(chat_type=ChatType.PRIVATE, state=OutBalance.number)
async def out_number(message: types.Message, state: FSMContext):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        if message.text != FAKE_NUMBER and message.text != f"+{FAKE_NUMBER}":
            await message.answer(payload.out_invreq_text,
                                 reply_markup=keyboards.main_keyboard())
            await state.finish()
        else:
            async with state.proxy() as data:
                user.balance -= data['amount']
                if user.balance < 0:
                    await message.answer("Ошибка!")
                    return
                user.save()
                CasinoUserHistory.create(cid=message.chat.id, amount=data['amount'],
                                         editor=1, balance=user.balance)

            await message.answer(f"Баланс: <b>{user.balance} RUB</b>\n" + payload.out_req_succesful,
                                 reply_markup=keyboards.main_keyboard())
            await state.finish()
    except CasinoUser.DoesNotExist:
        logger.debug(f"#{message.chat.id} - does not exist")


@dp.message_handler(Text(contains="промо", ignore_case=True),
                    chat_type=ChatType.PRIVATE, state="*")
async def insert_promo(message: types.Message):
    await message.answer("Введите промокод", reply_markup=keyboards.cancel_keyboard)
    await OutBalance.promo.set()


@dp.message_handler(chat_type=ChatType.PRIVATE, state=OutBalance.promo)
async def promo_complete(message: types.Message):
    try:
        user = CasinoUser.get(cid=message.chat.id)
        if message.text in PROMOS:
            amount = PROMOS[message.text]
            if user.bonus == amount:
                await message.answer("Такой промокод уже активирован", reply_markup=keyboards.selfcab_keyboard)
                return
            user.bonus = amount
            user.save()
            await message.answer(f"Промокод на {amount} RUB активирован!", reply_markup=keyboards.selfcab_keyboard)
        else:
            await message.answer("Такой промокод не удалось найти", reply_markup=keyboards.selfcab_keyboard)
    except CasinoUser.DoesNotExist:
        logger.info(f"CasinoUser {message.chat.id} does not exist")
    finally:
        await SelfCabine.main.set()
