import re
from datetime import timedelta
from configparser import NoOptionError
from asyncio.exceptions import TimeoutError

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiohttp.client_exceptions import ClientProxyConnectionError
from customutils.qiwiapi import get_currency, get_identification_level
from customutils.qiwiapi.exceptions import InvalidToken, InvalidAccount
from customutils.datefunc import normalized_local_now

from loader import dp
from config import config
from data import payload
from data.keyboards import *
from data.states import Qiwi
from utils.executional import find_token, get_api, delete_api_proxy, check_proxy


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
            api, proxy_url = get_api(token)
            try:
                profile = await api.get_profile()
                qiwiaccs = await api.get_balance()
                account = profile.contractInfo.contractId
                accounts.append(account)
                if qiwiaccs[0].currency == 643:
                    all_balance += qiwiaccs[0].balance.amount
            except (InvalidToken, InvalidAccount):
                await query.message.edit_text(
                    payload.qiwi_delete_text.format(
                        token=api.token[:8] + "*" * 24,
                    )
                )
                tokens.pop(i)
                config.edit_config("qiwi_tokens", tokens)
            except (
                ClientProxyConnectionError,
                TimeoutError,
            ):  # somethink wrong with connection
                proxy = delete_api_proxy(token)
                if proxy:
                    await query.message.answer(
                        payload.qiwi_proxy_delete.format(
                            proxy=proxy,
                            token=token[:8] + "*" * 24,
                        )
                    )
                    # add qiwi data to answer
                    api.proxy = None
                    profile = await api.get_profile()
                    qiwiaccs = await api.get_balance()
                    account = profile.contractInfo.contractId
                    accounts.append(account)
                    if qiwiaccs[0].currency == 643:
                        all_balance += qiwiaccs[0].balance.amount
                else:
                    await query.message.answer(payload.proxy_error_text)
            finally:
                await api.close()
        await query.message.edit_text(
            payload.qiwi_command_text.format(
                all_balance=all_balance,
            ),
            reply_markup=qiwi_keyboard(accounts),
        )

    except NoOptionError:
        await query.message.edit_text(
            payload.no_qiwis_text, reply_markup=add_qiwi_keyboard
        )


@dp.message_handler(commands="qiwi", admins_chat=True, is_admin=True)
async def qiwi_command(message: types.Message):
    try:
        tokens = config("qiwi_tokens")
        if isinstance(tokens, str):
            tokens = [tokens]

        all_balance = 0
        accounts = []
        for token in tokens:
            api, proxy_url = get_api(token)
            try:  # API requests
                profile = await api.get_profile()
                qiwiaccs = await api.get_balance()
                account = profile.contractInfo.contractId
                accounts.append(account)
                if qiwiaccs[0].currency == 643:
                    all_balance += qiwiaccs[0].balance.amount
            except (InvalidToken, InvalidAccount):
                await message.answer(
                    payload.qiwi_delete_text.format(
                        token=api.token[:8] + "*" * 24,
                    )
                )
                tokens.remove(token)
                config.edit_config("qiwi_tokens", tokens)
            except (ClientProxyConnectionError, TimeoutError):
                proxy = delete_api_proxy(token)
                if proxy:
                    await message.answer(
                        payload.qiwi_proxy_delete.format(
                            proxy=proxy,
                            token=api.token[:8] + "*" * 24,
                        )
                    )
                    # add conn error qiwi to answer
                    api.proxy = None
                    profile = await api.get_profile()
                    qiwiaccs = await api.get_balance()
                    account = profile.contractInfo.contractId
                    accounts.append(account)
                    if qiwiaccs[0].currency == 643:
                        all_balance += qiwiaccs[0].balance.amount
                else:
                    await message.answer(payload.qiwi_error_text)
            finally:  # close to except error
                await api.close()
        await message.answer(  # do shit
            payload.qiwi_command_text.format(
                all_balance=all_balance,
            ),
            reply_markup=qiwi_keyboard(accounts),
        )

    except NoOptionError:
        await message.answer(payload.no_qiwis_text, reply_markup=add_qiwi_keyboard)


@dp.callback_query_handler(text="add_qiwi", admins_chat=True, is_admin=True)
async def add_qiwi(query: types.CallbackQuery):
    await query.message.edit_text(
        "Введите киви токен в бота для безопасности данных.",
        reply_markup=cancel_keyboard,
    )
    await dp.bot.send_message(query.from_user.id, payload.add_qiwis_text)
    # set new state in bot not in admins chat
    state = dp.get_current().current_state(
        chat=query.from_user.id, user=query.from_user.id
    )
    await state.set_state(Qiwi.new)


@dp.message_handler(state=Qiwi.new, is_admin=True)
async def new_qiwi(message: types.Message, state: FSMContext):
    message.chat.id = config("admins_chat")  # change to send to admins
    proxy_regex = r"http:\/\/([a-zA-Z0-9]+:[a-zA-Z0-9]+@)*([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+)(:[0-9]+)*"
    data = message.text.split("\n")
    try:
        if re.fullmatch(proxy_regex, data[1].strip()):
            msg = await message.answer("Проверяю прокси... [3 seconds]")
            proxy_valid = await check_proxy(data[1].strip())
            if proxy_valid:
                proxy_data = f"({data[1].strip()})"
                await msg.delete()
            else:
                proxy_data = ""
                await msg.edit_text("Прокси не валидные! не добавляю в кивас.")
    except IndexError:
        proxy_data = ""

    if re.fullmatch(r"[a-f0-9]{32}", data[0].strip()):
        try:
            tokens = config("qiwi_tokens")
            if data[0].strip() in map(find_token, tokens):
                await message.answer(payload.same_qiwi_text)
                await state.finish()
                await qiwi_command(message)
                return

            if isinstance(tokens, str):
                config.edit_config("qiwi_tokens", f"{tokens},{data[0]}{proxy_data}")
            else:
                tokens.append(data[0].strip() + proxy_data)
                config.edit_config("qiwi_tokens", tokens)
        except NoOptionError:
            config.edit_config("qiwi_tokens", data[0].strip() + proxy_data)

        await state.finish()
        await qiwi_command(message)
    else:
        await message.answer(payload.invalid_newqiwi_text, reply_markup=cancel_keyboard)
        await state.finish()
        await qiwi_command(message)


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "addproxy", admins_chat=True, is_admin=True
)
async def qiwi_proxy(query: types.CallbackQuery):
    await query.message.edit_text(
        payload.qiwi_add_proxy_text, reply_markup=cancel_keyboard
    )
    await Qiwi.add_proxy.set()
    async with dp.current_state().proxy() as data:
        data["num"] = int(
            query.data.split("_")[1]
        )  # setting num of qiwi token in config


@dp.message_handler(state=Qiwi.add_proxy, admins_chat=True, is_admin=True)
async def add_qiwi_proxy(message: types.Message, state: FSMContext):
    regex = r"http:\/\/([a-zA-Z0-9]+:[a-zA-Z0-9]+@)*([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+)(:[0-9]+)*"
    if re.fullmatch(regex, message.text):  # check if it's a valid'
        msg = await message.answer("Проверяю прокси... 3 сек")
        proxy_valid = await check_proxy(message.text)
        if proxy_valid:
            await msg.delete()
        else:
            await msg.edit_text("Прокси невалид иди нах не добавлю)")
            await state.finish()
            await qiwi_command(message)  # /qiwi commands esadkasd
            return

        tokens = config("qiwi_tokens")
        if isinstance(tokens, list):  # if list than find the correct
            async with state.proxy() as data:
                try:  # setting token with proxy in ()
                    tokens[data["num"]] = f"{tokens[data['num']]}({message.text})"
                    config.edit_config("qiwi_tokens", tokens)
                    await message.answer(payload.new_proxy_success_text)
                    await state.finish()
                    await qiwi_command(message)  # /qiwi command
                except IndexError:
                    await message.answer(
                        payload.qiwi_add_proxy_text, reply_markup=cancel_keyboard
                    )
        else:  # simply edit
            config.edit_config("qiwi_tokens", f"{tokens}({message.text})")
            await message.answer(payload.new_proxy_success_text)
            await state.finish()
            await qiwi_command(message)  # /qiwi command
    else:  # if not matches
        await message.answer(payload.qiwi_add_proxy_text, reply_markup=cancel_keyboard)


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "qiwidelete", admins_chat=True, is_admin=True
)
async def qiwi_delete(query: types.CallbackQuery):
    num = query.data.split("_")[1]
    await query.message.edit_text(
        payload.qiwi_selfdelete_text, reply_markup=qiwi_delete_keyboard(num)
    )
    await Qiwi.delete.set()


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "suredelete",
    state=Qiwi.delete,
    admins_chat=True,
    is_admin=True,
)
async def qiwi_delete_sure(query: types.CallbackQuery, state: FSMContext):
    num = int(query.data.split("_")[1])
    tokens = config("qiwi_tokens")
    if isinstance(tokens, str):
        tokens = [tokens]

    await query.message.edit_text(
        payload.qiwi_delete_text.format(token=find_token(tokens[num][:8] + "*" * 24))
    )
    tokens.pop(num)
    config.edit_config("qiwi_tokens", tokens)

    await state.finish()
    await qiwi_command(query.message)


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "qiwi", admins_chat=True, is_admin=True
)
async def qiwi_info(query: types.CallbackQuery):
    try:
        tokens = config("qiwi_tokens")  # [str, str]
        num = query.data.split("_")[1]
        if isinstance(tokens, list):
            token = tokens[int(num)]
        elif num == "0":
            token = tokens
        api, proxy_url = get_api(token)
        if proxy_url is None:
            proxy_url = "Нету"

        try:
            profile = await api.get_profile()  # to answer as msg
            accs = await api.get_balance()
            history_stat = await api.get_statistics(
                normalized_local_now() - timedelta(days=10), normalized_local_now()
            )
            incoming = history_stat.incomingTotal[0]
            outgoing = history_stat.outgoingTotal[0]
            last_transactions = await api.get_transactions(rows=7)
            level = profile.contractInfo.identificationInfo[0].identificationLevel
        except (InvalidToken, InvalidAccount):
            await message.answer(
                payload.qiwi_delete_text.format(
                    token=token[:8] + "*" * 24,
                )
            )
            if isinstance(tokens, list):
                tokens.remove(token)
            else:
                tokens = None
            config.edit_config("qiwi_tokens", tokens)
        except (ClientProxyConnectionError, TimeoutError):
            proxy = delete_api_proxy(token)
            if proxy:
                await query.message.edit_text(
                    payload.qiwi_proxy_delete.format(
                        proxy=proxy,
                        token=token[:8] + "*" * 24,
                    )
                )
            else:
                await query.message.edit_text(payload.qiwi_error_text)
        finally:
            await api.close()

        balance = accs[0].balance
        last_actions = ""
        for action in last_transactions.data:
            action_type = (
                "Пополнение +"
                if action.trnsType == "IN"
                else "Перевод -"
                if action.trnsType == "OUT"
                else "Перевод с карты -"
            )
            action_currency = get_currency(action.total.currency)
            comment = (
                f"Комментарий: <b>{action.comment}</b>"
                if action.comment
                else "<i>Без комментария.</i>"
            )
            fdate = action.date.strftime("%d.%m.%Y в %H:%M")
            last_actions += f"{action_type}<b>{action.total.amount} {action_currency}</b>, {action.account}\n{comment}, {fdate}\n"
        await query.message.edit_text(
            payload.qiwi_info_text.format(
                number=profile.contractInfo.contractId,
                balance=f"{balance.amount} {get_currency(balance.currency)}",
                status=get_identification_level(level),
                proxy_url=proxy_url,
                incoming=f"{incoming.amount} {get_currency(incoming.currency)}",
                outgoing=f"{outgoing.amount} {get_currency(outgoing.currency)}",
                last_actions=last_actions,
            ),
            reply_markup=oneqiwi_keyboard(num),
        )
    except NoOptionError:
        await query.message.answer(payload.qiwi_error_text)
