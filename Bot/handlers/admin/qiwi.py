from datetime import datetime

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from loguru import logger

from qiwiapi import Qiwi, InvalidProxy
from customutils.datefunc import normalized_local_now
from loader import dp, config
from data.texts import (
    qiwi_emoji,
    no_qiwis_text,
    qiwi_to_bot_text,
    wanna_add_qiwi_text,
    add_qiwi_text,
    invalid_newqiwi_text,
    valid_newqiwi_text,
    qiwi_tokens_info_text,
    qiwi_info_text,
    qiwi_account_text,
    qiwi_action_text,
)
from data.keyboards import qiwi_keyboard, add_qiwi_keyboard, add_qiwi_sure_keyboard
from data.states import NewQiwi


async def proxy_invalid(qiwi: Qiwi):
    tokens = list(config.qiwi_tokens)
    tokens.remove({"token": qiwi.token, "proxy_url": qiwi.proxy})

    config.qiwi_tokens = tokens  # .edit(name, value)

    await dp.bot.send_message(config.admins_chat, qiwi.token[:16])


async def qiwi_tokens_info(chat_id: int):
    """
    info about qiwi tokens.
    without message to call it by another handler ANYWHERE.
    """
    if not config.qiwi_tokens:
        await dp.bot.send_message(
            chat_id, no_qiwis_text, reply_markup=add_qiwi_keyboard()
        )
    else:
        all_amounts = 0
        account_texts = []
        qiwi_numbers = []

        for qiwi_obj in config.qiwi_tokens:  # {"token": ..., "proxy_url": ...}
            qiwi = Qiwi(**qiwi_obj, on_invalid_proxy=proxy_invalid)

            try:
                accounts = await qiwi.get_accounts()
                profile = await qiwi.get_profile()
            except InvalidProxy:
                await dp.bot.send_message(chat_id, "ИнвалидПрокси")
                return  # some logic

            currency = accounts[0].balance.currency
            amount = accounts[0].balance.amount
            number = profile.authInfo.personId

            if currency == qiwi.RUB_CURRENCY:
                all_amounts += amount

            account_texts.append(
                qiwi_account_text.format(
                    amount=amount,
                    number=number,
                    currency=qiwi.get_currency(currency),
                )
            )
            qiwi_numbers.append(number)

            logger.debug(f"Get info about qiwi: {number=}, {amount=}")

        await dp.bot.send_message(
            chat_id,
            qiwi_tokens_info_text.format(
                qiwi_account_texts="\n".join(account_texts), all_amounts=all_amounts
            ),
            reply_markup=add_qiwi_keyboard(qiwi_numbers),  # can be None or []
        )


@dp.callback_query_handler(text="backqiwi", admins_chat=True, is_admin=True)
async def qiwi_back_command(query: CallbackQuery):
    await query.message.delete()
    await qiwi_tokens_info(query.message.chat.id)


@dp.message_handler(commands=["qiwi", "qiwis"], admins_chat=True, is_admin=True)
async def qiwi_command(message: Message):
    await message.reply(qiwi_emoji)  # qiwi_emoji_text
    await qiwi_tokens_info(message.chat.id)


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "qiwi", admins_chat=True, is_admin=True
)
async def qiwi_information(query: CallbackQuery):
    config_id = int(query.data.split("_")[1])
    qiwi_tokens = config.qiwi_tokens[config_id]
    qiwi = Qiwi(**qiwi_tokens)

    try:
        accounts = await qiwi.get_accounts()
        profile = await qiwi.get_profile()
        payments = await qiwi.get_payments(rows=10, operation=Qiwi.IN)

        datenow = normalized_local_now()

        total_payments = await qiwi.get_payments_total(
            datetime(datenow.year, datenow.month, datenow.day),
            datetime(datenow.year, datenow.month, datenow.day + 1),
        )
    except InvalidProxy:
        await query.message.answer("Прокси Инвалиды!! кодер сука")
        return  # some logic

    currency = accounts[0].balance.currency
    amount = accounts[0].balance.amount
    number = profile.authInfo.personId
    level = profile.contractInfo.identificationInfo

    # payments daily incoming
    incoming = ""
    if total_payments.incomingTotal:
        incoming = (
            f"+{total_payments.incomingTotal[0].amount} "
            f"{Qiwi.get_currency(total_payments.incomingTotal[0].currency)}"
        )
    # payments daily outgoing
    outgoing = ""
    if total_payments.outgoingTotal:
        outgoing = (
            f"-{total_payments.outgoingTotal[0].amount} "
            f"{Qiwi.get_currency(total_payments.outgoingTotal[0].currency)}"
        )

    qiwi_action_texts = []
    for transaction in payments.data:
        qiwi_action_texts.append(
            qiwi_action_text.format(
                going=f"+{transaction.sum.amount}",
                currency=Qiwi.get_currency(transaction.sum.currency),
                comment=transaction.comment if transaction.comment else "Без коммента",
            )
        )

    await query.message.edit_text(
        qiwi_info_text.format(
            number=number,
            amount=amount,
            currency=qiwi.get_currency(currency),
            incoming=incoming,
            outgoing=outgoing,
            status=qiwi.get_identification_level(level),
            proxy="Есть" if qiwi_tokens["proxy_url"] else "Нету",
            qiwi_action_texts="\n".join(qiwi_action_texts),
        ),
        reply_markup=qiwi_keyboard(config_id),
    )


@dp.callback_query_handler(text="qiwiadd", admins_chat=True, is_admin=True)
async def qiwi_add_admins(query: CallbackQuery):
    await query.message.edit_text(qiwi_to_bot_text)
    await dp.bot.send_message(
        query.from_user.id, wanna_add_qiwi_text, reply_markup=add_qiwi_sure_keyboard
    )


@dp.callback_query_handler(text="qiwiadd", admins_chat=False, is_admin=True)
async def qiwi_add_bot(query: CallbackQuery):
    await query.message.edit_text(add_qiwi_text)
    await NewQiwi.main.set()


@dp.message_handler(state=NewQiwi.main, is_admin=True)
async def qiwi_new(message: Message, state: FSMContext):
    data = message.text.split("\n")
    try:
        if len(data) >= 2:  # token and proxy and can be ...
            payload = {"token": data[0], "proxy_url": data[1]}
        else:  # only token
            payload = {"token": data[0], "proxy_url": None}

        Qiwi.validate(**payload)

        if isinstance(config.qiwi_tokens, list):
            qiwi_tokens = [*config.qiwi_tokens, payload]
        else:
            qiwi_tokens = [payload]

        logger.info(f"Setting up {qiwi_tokens=} in BotsConfig")
        config.qiwi_tokens = qiwi_tokens

        await message.answer(valid_newqiwi_text)
        await qiwi_tokens_info(config.admins_chat)

        await state.finish()
    except ValueError:
        await message.answer(invalid_newqiwi_text)
