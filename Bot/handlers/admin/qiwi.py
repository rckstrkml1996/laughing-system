import re
from configparser import NoOptionError

from aiogram import types
from aiogram.dispatcher import FSMContext
from customutils.qiwiapi import QiwiApi, get_currency, get_identification_level
from customutils.qiwiapi.exceptions import InvalidToken, InvalidAccount

from loader import dp
from config import config
from data import payload
from data.keyboards import *
from data.states import Qiwi


# говнокод лень фиксить)
@dp.callback_query_handler(text="backqiwi", admins_chat=True, is_admin=True)
async def back_to_qiwi_command(query: types.CallbackQuery):
    try:
        tokens = config("qiwi_tokens")
        if isinstance(tokens, str):
            tokens = [tokens]

        all_balance = 0
        accounts = []
        for token in tokens:
            api = QiwiApi(token)
            try:
                profile = await api.get_profile()
                qiwiaccs = await api.get_balance()
                account = profile.contractInfo.contractId
                accounts.append(account)
                if qiwiaccs[0].currency == 643:
                    all_balance += qiwiaccs[0].balance.amount
            except (InvalidToken, InvalidAccount):
                await query.message.edit_text(payload.qiwi_delete.format(
                    token=token[:8] + "*" * 24,
                ))
                tokens.pop(i)
                config.edit_config("qiwi_tokens", tokens)
            finally:
                await api.close()
        await query.message.edit_text(payload.qiwi_command_text.format(
            all_balance=all_balance,
        ), reply_markup=qiwi_keyboard(accounts))

    except NoOptionError:
        await query.message.edit_text(payload.no_qiwis_text, reply_markup=add_qiwi_keyboard)


@dp.message_handler(commands="qiwi", admins_chat=True, is_admin=True)
async def qiwi_command(message: types.Message):
    try:
        tokens = config("qiwi_tokens")
        if isinstance(tokens, str):
            tokens = [tokens]

        all_balance = 0
        accounts = []
        for token in tokens:
            api = QiwiApi(token)
            try:
                profile = await api.get_profile()
                qiwiaccs = await api.get_balance()
                account = profile.contractInfo.contractId
                accounts.append(account)
                if qiwiaccs[0].currency == 643:
                    all_balance += qiwiaccs[0].balance.amount
            except (InvalidToken, InvalidAccount):
                await message.answer(payload.qiwi_delete.format(
                    token=token[:8] + "*" * 24,
                ))
                tokens.pop(i)
                config.edit_config("qiwi_tokens", tokens)
            finally:
                await api.close()
        await message.answer(payload.qiwi_command_text.format(
            all_balance=all_balance,
        ), reply_markup=qiwi_keyboard(accounts))

    except NoOptionError:
        await query.message.edit_text(payload.no_qiwis_text, reply_markup=add_qiwi_keyboard)


@dp.callback_query_handler(text="add_qiwi", admins_chat=True, is_admin=True)
async def add_qiwi(query: types.CallbackQuery):
    await query.message.edit_text(payload.add_qiwis_text, reply_markup=cancel_keyboard)
    await Qiwi.new.set()


@dp.message_handler(state=Qiwi.new, admins_chat=True)
async def new_qiwi(message: types.Message, state: FSMContext):
    data = message.text.split("\n")
    if re.fullmatch(r'[a-f0-9]{32}', data[0].strip()):
        try:
            tokens = config("qiwi_tokens")
            if not isinstance(tokens, list):
                config.edit_config("qiwi_tokens", f'{tokens},{data[0]}')
            else:
                tokens.append(data[0])
                config.edit_config("qiwi_tokens", tokens)
        except NoOptionError:
            config.edit_config("qiwi_tokens", data[0])
        await qiwi_command(message)
        await state.finish()
    else:
        await message.answer(payload.invalid_newqiwi_text, reply_markup=cancel_keyboard)


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "qiwi", admins_chat=True, is_admin=True)
async def qiwi_info(query: types.CallbackQuery):
    try:
        tokens = config("qiwi_tokens")  # [str, str]
        num = query.data.split("_")[1]
        if isinstance(tokens, list):
            token = tokens[int(num)]
        elif num == "0":
            token = tokens
        api = QiwiApi(token)

        try:
            profile = await api.get_profile()  # to answer as msg
            accs = await api.get_balance()
            last_transactions = await api.get_transactions(rows=10)
            level = profile.contractInfo.identificationInfo[0].identificationLevel
        except (InvalidToken, InvalidAccount):
            await message.answer(payload.qiwi_delete.format(
                token=token[:8] + "*" * 24,
            ))
            tokens.pop(i)
            config.edit_config("qiwi_tokens", tokens)
        finally:
            await api.close()

        balance = accs[0].balance
        last_actions = ""
        for action in last_transactions.data:
            action_type = "Пополнение +" if action.trnsType == "IN" else "Перевод -" if action.trnsType == "OUT" else "Перевод с карты -"
            action_currency = get_currency(action.total.currency)
            comment = f'Комментарий: <b>{action.comment}</b>' if action.comment else "<i>Без комментария.</i>"
            fdate = action.date.strftime("%m.%d.%Y в %H:%M")
            last_actions += f'{action_type}<b>{action.total.amount} {action_currency}</b>, {action.account}\n{comment}, {fdate}\n'
        await query.message.edit_text(payload.qiwi_info_text.format(
            number=profile.contractInfo.contractId,
            balance=f'{balance.amount} {get_currency(balance.currency)}',
            status=get_identification_level(level),
            last_actions=last_actions
        ), reply_markup=backqiwi_keyboard
        )
    except NoOptionError:
        await query.message.answer(payload.qiwi_error_text)
