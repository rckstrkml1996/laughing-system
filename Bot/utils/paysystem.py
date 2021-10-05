from asyncio import sleep
from asyncio.exceptions import TimeoutError
from datetime import timedelta
from configparser import NoOptionError

from loguru import logger
from aiohttp.client_exceptions import ClientProxyConnectionError
from aiogram.types.input_file import InputFile
from customutils.datefunc import datetime_local_now
from customutils.models import QiwiPayment, Profit
from customutils.models import CasinoPayment, EscortPayment, TradingPayment
from customutils.qiwiapi import QiwiPaymentsParser
from customutils.qiwiapi.types import Payments, Transaction

from loader import dp, db_commands
from config import config, ServiceNames
from data import payload
from data.keyboards import profit_pay_keyboard
from utils.executional import get_api, delete_api_proxy
from .render import render_profit


async def check_casino(traction: Transaction) -> bool:
    delta = datetime_local_now() - timedelta(days=3)
    try:
        del_count = (
            CasinoPayment.delete().where(CasinoPayment.created < delta).execute()
        )
        if del_count != 0:
            logger.info(f"Casino deleting old payments: {del_count}")
    except Exception as e:
        logger.exception(e)

    if traction.trnsType != "IN":
        return False
    try:
        pay = CasinoPayment.get(comment=traction.comment)

        if pay.amount <= traction.transactionSum.amount and pay.done == 0:
            logger.debug(f"Some payment with {pay.amount} amount")
            if traction.transactionSum.currency == 643:
                pay.done = 1
                pay.save()
                logger.info(
                    f"Apply payment {pay.amount} amount in base and making pay."
                )

                casino_user = pay.owner
                worker = casino_user.owner

                paymnts_count = CasinoPayment.where(
                    CasinoPayment.owner.id == casino_user.id, CasinoPayment.done == 1
                ).count()
                logger.debug(f"Payments count: {paymnts_count}")
                xpay = "" if paymnts_count == 0 else f"X{paymnts_count} "

                service_num = 0
                service = xpay + ServiceNames[service_num]  # thats casino

                moll = 0.8 if paymnts_count <= 1 else 0.7
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
                logger.debug("Sucessfully created QiwiPayment and Profit in base.")

                return await send_profit(profit, moll, service, pay)
    except CasinoPayment.DoesNotExist:
        logger.debug(f"Casino payment with comment {traction.comment} not in base!")

    return False


async def check_escort(traction: Transaction) -> bool:
    delta = datetime_local_now() - timedelta(days=3)
    del_count = EscortPayment.delete().where(EscortPayment.created < delta).execute()
    if del_count != 0:
        logger.info(f"Escort deleting old payments: {del_count}")

    if traction.trnsType != "IN":
        return False
    try:
        pay = EscortPayment.get(comment=traction.comment)

        logger.debug(f"Some payment with {traction.total.amount} amount")
        if traction.transactionSum.currency == 643 and pay.done == 0:
            pay.done = 1
            pay.amount = traction.total.amount
            pay.save()

            logger.info(f"Apply payment {pay.amount} amount in base and making pay.")

            escort_user = pay.owner
            worker = escort_user.owner

            paymnts_count = EscortPayment.where(
                EscortPayment.owner == escort_user, EscortPayment.done == 1
            ).count()
            xpay = "" if paymnts_count == 0 else f"X{paymnts_count} "

            service_num = 1
            service = xpay + ServiceNames[service_num]  # thats escort

            moll = 0.8 if paymnts_count <= 1 else 0.7
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
            logger.debug("Sucessfully created QiwiPayment and Profit in base.")

            return await send_profit(profit, moll, service, pay)
    except EscortPayment.DoesNotExist:
        logger.debug(f"Escort payment with comment {traction.comment} not in base!")

    return False


async def check_trading(traction: Transaction) -> bool:
    delta = datetime_local_now() - timedelta(days=3)
    del_count = TradingPayment.delete().where(TradingPayment.created < delta).execute()
    if del_count != 0:
        logger.info(f"Trading deleting old payments: {del_count}")

    if traction.trnsType != "IN":
        return False
    try:
        pay = TradingPayment.get(comment=traction.comment)

        if pay.amount <= traction.transactionSum.amount and pay.done == 0:
            logger.debug(f"Some payment with {traction.total.amount} amount")
            if traction.transactionSum.currency == 643:
                pay.done = 1
                pay.save()

                logger.info(
                    f"Apply payment {pay.amount} amount in base and making pay."
                )

                trading_user = pay.owner
                worker = trading_user.owner

                paymnts_count = TradingPayment.where(
                    TradingPayment.owner == trading_user, TradingPayment.done == 1
                ).count()
                xpay = "" if paymnts_count == 0 else f"X{paymnts_count} "

                service_num = 2
                service = xpay + ServiceNames[service_num]  # thats trading

                moll = 0.8 if paymnts_count <= 1 else 0.7
                share = int(pay.amount * moll)

                # if trading_user.fuckedup:
                # trading_user.fuckedup = False
                # trading_user.save()

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
                logger.debug("Sucessfully created QiwiPayment and Profit in base.")

                return await send_profit(profit, moll, service, pay)
    except TradingPayment.DoesNotExist:
        logger.debug(f"Trading payment with comment {traction.comment} not in base!")

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
            elif await check_trading(transaction):  # check
                service = "Трейдинг"
                logger.info(
                    f"Trading, new payment in active qiwi {transaction.personId} sum: {transaction.total.amount}"
                )
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
    except Exception as ex:
        logger.error(ex)


async def check_qiwis():
    try:
        token = config("qiwi_tokens")
        if isinstance(token, list):
            token = token[0]

        api, proxy_url = get_api(token)  # get api instance by token(proxy) string
        parser = QiwiPaymentsParser(api, on_new_payment)
    except NoOptionError:
        token = None

    logger.debug("QiwiPaymentsParser started succesfully.")
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
                logger.debug(f"Check qiwi [{parser.api.token}] payments")
            except (ClientProxyConnectionError, TimeoutError):
                delete_api_proxy(token)
                logger.warning("Deleting Qiwi - Lock [TErr, ClErr]")
            except Exception as e:
                logger.exception(e)
                # update qiwi
                token = new_token
                api, proxy_url = get_api(token)
                parser = QiwiPaymentsParser(api, on_new_payment)
                logger.info(f"Parsing payments with new qiwi {token}")
            finally:
                await parser.api.close()
        except NoOptionError:
            token = None

        await sleep(60)


async def send_profit(profit: Profit, moll, service: str, payment=None):
    worker = profit.owner

    all_profit = db_commands.get_profits_sum(worker.id)
    profit_path = render_profit(
        all_profit, profit.amount, profit.share, service, worker.username
    )
    logger.debug(
        f"Succesfully rendered profit path: {profit_path}, sending to outs chat"
    )
    profit_text = str(
        payload.profit_text.format(
            service=service,
            share=profit.share,
            amount=profit.amount,
            cid=worker.cid,
            name=worker.username if worker.username else worker.name,
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
