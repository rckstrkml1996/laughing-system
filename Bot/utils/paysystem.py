# from time import time
from asyncio import sleep
from asyncio.exceptions import TimeoutError
from configparser import NoOptionError

from aiohttp.client_exceptions import ClientProxyConnectionError
from aiogram.types.input_file import InputFile
from aiogram.utils.emoji import emojize
from loguru import logger

from customutils.models import QiwiPayment, Profit
from customutils.models import CasinoPayment, EscortPayment, TradingPayment
from customutils.qiwiapi import QiwiPaymentsParser, get_api
from customutils.qiwiapi.types import Payments, Transaction

from loader import dp, db_commands
from config import config, ServiceNames
from data import payload
from data.keyboards import profit_pay_keyboard
from utils.executional import delete_api_proxy
from .render import render_profit

# 0 - not done
# 1 - real done
# 2 - fake done
async def check_casino(traction: Transaction) -> bool:
    if traction.trnsType != "IN":
        return False

    if traction.transactionSum.currency != 643:
        return False

    try:
        pay = CasinoPayment.get(comment=traction.comment)

        if traction.transactionSum.amount >= pay.amount:
            logger.debug(
                f"Some new payment with {pay.amount=} {traction.transactionSum.currency}"
            )

            pay.done = 1  # (real done)
            pay.save()

            logger.info(f"For pay {pay.amount=} set {pay.done=} and making pay.")

            casino_user = pay.owner
            worker = casino_user.owner

            payments_count = db_commands.get_payments_count(CasinoPayment, casino_user)
            logger.debug(f"Payments count: {payments_count}")

            service_num = 0
            service = f"X{payments_count} {ServiceNames[service_num]}"  # thats casino

            moll = 0.8 if payments_count <= 1 else 0.7
            share = int(pay.amount * moll)

            qiwi_pay = QiwiPayment.create(
                person_id=traction.personId,
                account=traction.account,
                amount=traction.total.amount,
                currency=traction.total.currency,
                comment=traction.comment,
                date=traction.date,
            )
            profit = Profit.create(
                owner=worker,
                amount=int(pay.amount),
                share=share,
                service=service_num,
                payment=qiwi_pay,
            )
            logger.debug(
                "Sucessfully created QiwiPayment and Profit in base. sending.."
            )
            logger.debug(f"Sending profit, {moll=} {payments_count=}")

            return await send_profit(profit, moll, service, pay)
    except CasinoPayment.DoesNotExist:
        logger.debug(f"Casino payment with comment {traction.comment} not in base!")

    return False


async def check_escort(traction: Transaction) -> bool:
    if traction.trnsType != "IN":
        return False

    if traction.transactionSum.currency != 643:
        return False

    try:
        pay = EscortPayment.get(comment=traction.comment)

        if traction.transactionSum.amount >= pay.three_amount:
            pay.done = 3  # hour - two_hours - night
            pay.save()
        elif traction.transactionSum.amount >= pay.two_amount:
            pay.done = 2  # hour - two_hours - night
            pay.save()
        elif traction.transactionSum.amount >= pay.amount:
            pay.done = 1  # hour - two_hours - night
            pay.save()
        else:
            return False

        logger.info(
            f"Escort - Some new payment with {pay.amount=} {traction.transactionSum.currency}"
        )

        escort_user = pay.owner
        worker = escort_user.owner

        payments_count = (
            EscortPayment.select()
            .where(
                (EscortPayment.owner == escort_user) & (EscortPayment.done == 1)
                | (EscortPayment.done == 2)
                | (EscortPayment.done == 3)
            )
            .count()
        )
        logger.debug(f"Escort - Payments count: {payments_count}")

        service_num = 1
        service = f"X{payments_count} {ServiceNames[service_num]}"  # thats casino

        moll = 0.8 if payments_count <= 1 else 0.7
        share = int(pay.amount * moll)

        qiwi_pay = QiwiPayment.create(
            person_id=traction.personId,
            account=traction.account,
            amount=traction.total.amount,
            currency=traction.total.currency,
            comment=traction.comment,
            date=traction.date,
        )
        profit = Profit.create(
            owner=worker,
            amount=int(pay.amount),
            share=share,
            service=service_num,
            payment=qiwi_pay,
        )
        logger.debug(f"Created QiwiPayment and Profit. Sending profit {service=}")

        return await send_profit(profit, moll, service, pay)
    except EscortPayment.DoesNotExist:
        logger.debug(f"EscortPayment with comment {traction.comment} not in base!")

    return False


async def on_new_payment(payments: Payments):
    logger.info(f"On new payments {len(payments.data)} notify.")
    try:
        for transaction in payments.data:
            if await check_casino(transaction):  # check if supply on casino
                service = "Казино"
                logger.info(
                    f"Casino, new payment in active qiwi {transaction.personId} sum: {transaction.total.amount}"
                )
            elif await check_escort(transaction):  # check if on escort
                service = "Эскорт"
                logger.info(
                    f"Escort, new payment in active qiwi {transaction.personId} sum: {transaction.total.amount}"
                )
            # elif await check_trading(transaction):  # check
            #     service = "Трейдинг"
            #     logger.info(
            #         f"Trading, new payment in active qiwi {transaction.personId} sum: {transaction.total.amount}"
            #     )
            else:
                service = "Без сервиса"
                qiwi_pay = QiwiPayment.create(
                    person_id=transaction.personId,
                    account=transaction.account,
                    amount=transaction.total.amount,
                    payment_type=transaction.trnsType,
                    currency=transaction.total.currency,
                    comment=transaction.comment,
                    date=transaction.date,
                )

            comment = (
                f"Комментарий: <b>{transaction.comment}</b>"
                if transaction.comment
                else ":)"
            )
            await dp.bot.send_message(
                config("admins_chat"),
                f"{service}, в {transaction.personId}\nСумма: <b>{transaction.total.amount} RUB</b>\n{comment}",
            )

            payments_count = 0

            payments_count += db_commands.delete_old_payments(CasinoPayment)
            payments_count += db_commands.delete_old_payments(EscortPayment)
            payments_count += db_commands.delete_old_payments(TradingPayment)

            logger.info(f"Deleted {payments_count} payments.")
    except Exception as ex:
        logger.exception(ex)


async def check_qiwis():
    try:
        token = config("qiwi_tokens")
        if isinstance(token, list):
            token = token[0]

        api, proxy_url = get_api(token)  # get api instance by token(proxy) string
        parser = QiwiPaymentsParser(api, on_new_payment)
    except NoOptionError:
        token = None

    # logger.debug("QiwiPaymentsParser started succesfully.")
    while True:
        try:
            new_token = config("qiwi_tokens")
            if isinstance(new_token, list):
                new_token = new_token[0]

            if new_token != token:
                token = new_token
                api, proxy_url = get_api(token)
                parser = QiwiPaymentsParser(api, on_new_payment)
                logger.info(f"Parsing payments with new qiwi {token}")

            try:
                await parser.check()
                logger.debug(f"Checked qiwi [{parser.api.token}] payments.")
            except (ClientProxyConnectionError, TimeoutError):
                delete_api_proxy(token)
                logger.warning("Deleting Qiwi - Lock [TErr, ClErr]")
            except Exception as ex:
                logger.exception(ex)
                # update qiwi
                token = new_token
                api, proxy_url = get_api(token)
                parser = QiwiPaymentsParser(api, on_new_payment)
                logger.info(f"Parsing payments with new qiwi {token}")
            finally:
                await parser.api.close()
        except NoOptionError:
            token = None

        await sleep(config("qiwi_check_time"), int)


async def send_profit(profit: Profit, moll, service: str, payment=None):
    worker = profit.owner

    name = "Скрыт."
    link = emojize("Скрылся :green_heart:")
    if not worker.username_hide:
        name = worker.username if worker.username else worker.name
        link = f"<a href='tg://user?id={worker.cid}'>{name}</a>"

    all_profit = db_commands.get_profits_sum(worker.id)
    profit_path = render_profit(all_profit, profit.amount, profit.share, service, name)
    logger.debug(
        f"Succesfully rendered profit path: {profit_path}, sending to outs chat"
    )

    profit_text = str(
        payload.profit_text.format(
            service=service,
            share=profit.share,
            amount=profit.amount,
            link=link,
        ),
    )

    msg = await dp.bot.send_photo(
        config("outs_chat"),
        InputFile(profit_path),
        caption=profit_text,
    )

    stick_id = None
    try:
        stick_id = config("profit_sticker_id")
    except NoOptionError:
        await dp.bot.send_message(config("admins_chat"), "Задай стик к профита ежжи)")

    if stick_id:
        await dp.bot.send_sticker(
            config("workers_chat"),
            stick_id,
        )  # Sticker's id
    await dp.bot.send_message(config("workers_chat"), profit_text)

    profit.msg_url = msg.url  # save then send
    profit.save()

    if payment is None:
        logger.info("Making Fake Profit!")
        await dp.bot.send_message(
            worker.cid,
            payload.profit_worker_text.format(
                service=service,
                share=profit.share,
                amount=profit.amount,
                mid="незнаюблядь",
            ),
        )
        await dp.bot.send_message(
            config("admins_chat"),
            payload.admins_profit_text.format(
                profit_link=msg.url,
                cid=worker.cid,
                name=worker.username if worker.username else worker.name,
                service=service,
                amount=profit.amount,
                share=profit.share,
                moll=int(moll * 100),
                create_date="хз",
                pay_date="хз",
            ),
            reply_markup=profit_pay_keyboard(profit.id),
        )
        logger.debug("Succesfully sent to outs and admins chat")
    else:
        await dp.bot.send_message(
            worker.cid,
            payload.profit_worker_text.format(
                service=service,
                share=profit.share,
                amount=profit.amount,
                mid=payment.owner.id,
            ),
        )
        await dp.bot.send_message(
            config("admins_chat"),
            payload.admins_profit_text.format(
                profit_link=msg.url,
                cid=worker.cid,
                name=worker.username if worker.username else worker.name,
                service=service,
                amount=profit.amount,
                share=profit.share,
                moll=int(moll * 100),
                create_date=payment.created.strftime("%m.%d в %H:%M"),
                pay_date=profit.payment.date.strftime(
                    "%m.%d в %H:%M"
                ),  # profit.payment is qiwi!
            ),
            reply_markup=profit_pay_keyboard(profit.id),
        )
        logger.debug("Succesfully sent to outs and admins chat")
        return True
