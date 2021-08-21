from aiogram import types
from aiogram.dispatcher import FSMContext
from customutils.qiwiapi import QiwiApi, get_currency
from customutils.qiwiapi.exceptions import InvalidToken, InvalidAccount

from loader import dp
from config import config
from data import payload
from data.keyboards import *
from data.states import Qiwi


# говнокод лень фиксить)
@dp.callback_query_handler(text="backqiwi", admins_type=True)
async def back_to_qiwi_command(query: types.CallbackQuery):
    if query.from_user.id not in config("admins_id"):
        return
    try:
        accounts = config("qiwi_accs", str)
        tokens = config("qiwi_tokens")
        if not isinstance(accounts, list) and not isinstance(tokens, list):
            api = QiwiApi(tokens, accounts)
            try:
                qiwiacc = await api.get_balance()
                await api.close()
            except (InvalidToken, InvalidAccount):
                await query.message.edit_text(payload.qiwi_delete.format(
                    account=accounts,
                    token=tokens,
                ))
                config.edit_config("qiwi_accs", None)
                config.edit_config("qiwi_tokens", None)
                await api.close()
                await query.message.edit_text(payload.no_qiwis_text, reply_markup=add_qiwi_keyboard)
                return
            all_balance = qiwiacc[0].balance.amount
            await query.message.edit_text(payload.qiwi_command_text.format(
                all_balance=all_balance,
            ), reply_markup=qiwi_keyboard([accounts]))
        elif len(accounts) == len(tokens):
            all_balance = 0
            for i, token in enumerate(tokens):
                api = QiwiApi(token, accounts[i])
                try:
                    qiwiaccs = await api.get_balance()
                    if qiwiaccs[0].currency == 643:
                        all_balance += qiwiaccs[0].balance.amount
                except (InvalidToken, InvalidAccount):
                    await query.message.edit_text(payload.qiwi_delete.format(
                        account=accounts[i],
                        token=tokens[i],
                    ))
                    accounts.pop(i)
                    config.edit_config("qiwi_accs", accounts)
                    tokens.pop(i)
                    config.edit_config("qiwi_tokens", tokens)
                finally:
                    await api.close()
            await query.message.edit_text(payload.qiwi_command_text.format(
                all_balance=all_balance,
            ), reply_markup=qiwi_keyboard(accounts))
        else:
            await query.message.edit_text(payload.qiwi_error_text)
    except NoOptionError:
        await query.message.edit_text(payload.no_qiwis_text, reply_markup=add_qiwi_keyboard)


@dp.message_handler(commands="qiwi", admins_type=True)
async def qiwi_command(message: types.Message):
    if message.from_user.id not in config("admins_id"):
        return
    try:
        accounts = config("qiwi_accs", str)
        tokens = config("qiwi_tokens")
        if not isinstance(accounts, list) and not isinstance(tokens, list):
            api = QiwiApi(tokens, accounts)
            try:
                qiwiacc = await api.get_balance()
                await api.close()
            except (InvalidToken, InvalidAccount):
                await message.answer(payload.qiwi_delete.format(
                    account=accounts,
                    token=tokens,
                ))
                config.edit_config("qiwi_accs", None)
                config.edit_config("qiwi_tokens", None)
                await api.close()
                await message.answer(payload.no_qiwis_text, reply_markup=add_qiwi_keyboard)
                return
            all_balance = qiwiacc[0].balance.amount
            await message.answer(payload.qiwi_command_text.format(
                all_balance=all_balance,
            ), reply_markup=qiwi_keyboard([accounts]))
        elif len(accounts) == len(tokens):
            all_balance = 0
            for i, token in enumerate(tokens):
                api = QiwiApi(token, accounts[i])
                try:
                    qiwiaccs = await api.get_balance()
                    if qiwiaccs[0].currency == 643:
                        all_balance += qiwiaccs[0].balance.amount
                except (InvalidToken, InvalidAccount):
                    await message.answer(payload.qiwi_delete.format(
                        account=accounts[i],
                        token=tokens[i],
                    ))
                    accounts.pop(i)
                    config.edit_config("qiwi_accs", accounts)
                    tokens.pop(i)
                    config.edit_config("qiwi_tokens", tokens)
                finally:
                    await api.close()
            await message.answer(payload.qiwi_command_text.format(
                all_balance=all_balance,
            ), reply_markup=qiwi_keyboard(accounts))
        else:
            await message.answer(payload.qiwi_error_text)
    except NoOptionError:
        await message.answer(payload.no_qiwis_text, reply_markup=add_qiwi_keyboard)


@dp.callback_query_handler(text="add_qiwi", admins_type=True)
async def add_qiwi(query: types.CallbackQuery):
    if query.from_user.id not in config("admins_id"):
        return
    await query.message.edit_text(payload.add_qiwis_text, reply_markup=cancel_keyboard)
    await Qiwi.new.set()


@dp.message_handler(state=Qiwi.new, admins_type=True)
async def new_qiwi(message: types.Message, state: FSMContext):
    data = message.text.split("\n")
    if len(data) == 2:
        if re.fullmatch(r'[a-f0-9]{32}', data[1].strip()) and re.fullmatch(r'(7\d{10}|3\d{11}|77\d{9})', data[0].strip()):
            try:
                accounts = config("qiwi_accs", str)
                tokens = config("qiwi_tokens")
                if not isinstance(accounts, list):
                    if data[0].strip() == accounts:
                        await message.answer(payload.same_qiwi_text)
                        return
                    config.edit_config("qiwi_accs", f'{accounts},{data[0]}')
                else:
                    if data[0].strip() in accounts:
                        await message.answer(payload.same_qiwi_text)
                        await state.finish()
                        await qiwi_command(message)
                        return
                    accounts.append(data[0])
                    config.edit_config("qiwi_accs", accounts)
                if not isinstance(tokens, list):
                    config.edit_config("qiwi_tokens", f'{tokens},{data[1]}')
                else:
                    tokens.append(data[1])
                    config.edit_config("qiwi_tokens", tokens)
            except NoOptionError:
                config.edit_config("qiwi_accs", data[0])
                config.edit_config("qiwi_tokens", data[1])
            await qiwi_command(message)
            await state.finish()
    else:
        await message.answer(payload.invalid_newqiwi_text, reply_markup=cancel_keyboard)


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "qiwi", admins_type=True)
async def qiwi_info(query: types.CallbackQuery):
    if query.from_user.id not in config("admins_id"):
        return
    try:
        accounts = config("qiwi_accs", str)  # [str, str]
        tokens = config("qiwi_tokens")  # [str, str]
        number = query.data.split("_")[1]
        try:
            if isinstance(tokens, list):
                token = tokens[accounts.index(number)]
            elif accounts == number:
                token = tokens
            else:
                # await query.message.answer(payload.qiwi_error_text)
                return

            api = QiwiApi(token, number)

            accs = await api.get_balance()
            last_transactions = await api.get_transactions(rows=20)
            await api.close()

            balance = accs[0].balance
            last_actions = ""
            for action in last_transactions.data:
                action_type = "Пополнение +" if action.trnsType == "IN" else "Перевод -" if action.trnsType == "OUT" else "Перевод с карты -"
                action_currency = get_currency(action.total.currency)
                comment = f'Комментарий: <b>{action.comment}</b>' if action.comment else "<i>Без комментария.</i>"
                fdate = action.date.strftime("%m.%d.%Y в %H:%M")
                last_actions += f'{action_type}<b>{action.total.amount} {action_currency}</b>, {action.account}\n{comment}, {fdate}\n\n'
            await query.message.edit_text(payload.qiwi_info_text.format(
                number=number,
                balance=f'{balance.amount} {get_currency(balance.currency)}',
                last_actions=last_actions
            ), reply_markup=backqiwi_keyboard
            )
        except ValueError:
            pass
        except IndexError:
            pass
    except NoOptionError:
        await query.message.answer(payload.qiwi_error_text)
