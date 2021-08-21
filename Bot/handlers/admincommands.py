import re
from configparser import NoOptionError
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from customutils.models import Worker, CasinoUser
from customutils.qiwiapi import QiwiApi, get_currency
from customutils.qiwiapi.exceptions import InvalidToken, InvalidAccount

from loader import dp, casino_bot
from data import payload
from data.states import Pin, Qiwi, Alert
from data.keyboards import *
from utils.pinner import format_pin_text
from utils.executional import new_pin_text
from config import config


@dp.message_handler(commands="work", admins_type=True)
async def work_command(message: types.Message):
    casino_work = config("casino_work")
    escort_work = config("escort_work")
    antikino_work = config("antikino_work")

    all_work = casino_work and escort_work and antikino_work

    await message.answer(
        payload.adm_work_command.format(
            services_status=emojize(
                payload.services_status.format(
                    casino_status=f":full_moon: Казино СКАМ" if casino_work else f":new_moon: <del>Казино СКАМ</del>",
                    escort_status=f":full_moon: Эскорт СКАМ" if escort_work else f":new_moon: <del>Эскорт СКАМ</del>",
                    antikino_status=f":full_moon: Антикино СКАМ" if antikino_work else f":new_moon: <del>Антикино СКАМ</del>",
                    team_status=":full_moon: Общий статус: Ворк" if all_work else ":new_moon: Общий статус: Не ворк",
                )
            )
        ),
        reply_markup=admworkstatus_keyboard(all_work)
    )


@dp.callback_query_handler(text="toggleworkstatus", admins_type=True)
async def toggle_work_status(query: types.CallbackQuery):
    if query.from_user.id not in config("admins_id"):
        await query.answer("Ты не админ!")
        return

    casino_work = not config("casino_work")  # return bool values
    escort_work = not config("escort_work")
    antikino_work = not config("antikino_work")

    config.edit_config("casino_work", casino_work)
    config.edit_config("escort_work", escort_work)
    config.edit_config("antikino_work", antikino_work)

    all_work = casino_work and escort_work and antikino_work

    text = payload.adm_work_command.format(
        services_status=emojize(
            payload.services_status.format(
                casino_status=f":full_moon: Казино СКАМ" if casino_work else f":new_moon: <del>Казино СКАМ</del>",
                escort_status=f":full_moon: Эскорт СКАМ" if escort_work else f":new_moon: <del>Эскорт СКАМ</del>",
                antikino_status=f":full_moon: Антикино СКАМ" if antikino_work else f":new_moon: <del>Антикино СКАМ</del>",
                team_status=":full_moon: Общий статус: Ворк" if all_work else ":new_moon: Общий статус: Не ворк",
            )
        )
    )

    try:
        await query.message.edit_text(
            text, reply_markup=admworkstatus_keyboard(all_work)
        )
    except MessageNotModified:
        pass
    await dp.bot.send_message(config("workers_chat"), payload.setwork_text if all_work else payload.setdontwork_text)


""" WORKING FILE IDS AND CHANGING PHOTOS """


@dp.message_handler(content_types=["photo"], admins_type=True)
async def photo_hash(message: types.Message):
    if message.from_user.id not in config("admins_id"):
        return

    if message.caption == "/get_id":
        await message.answer(message.photo[-1].file_id)


@dp.message_handler(commands="new_design", admins_type=True)
async def new_design_command(message: types.Message):
    if message.from_user.id not in config("admins_id"):
        return


@dp.message_handler(commands="pinned", admins_type=True)
async def pinned_command(message: types.Message):
    if message.from_user.id not in config("admins_id"):
        return

    await message.answer(payload.pin_text())
    await message.reply(payload.pin_help_text, reply_markup=change_pin_keyboard)


@dp.callback_query_handler(text="change_pin", admins_type=True)
async def change_pin(query: types.CallbackQuery):
    if query.from_user.id not in config("admins_id"):
        await query.answer("Ты не админ)")
        return

    await query.message.answer("Введите новый текст для закрепа:")
    await Pin.change.set()


@dp.message_handler(state=Pin.change, admins_type=True)
async def new_pin(message: types.Message, state: FSMContext):
    await message.answer(message.text, reply_markup=new_pin_keyboard)
    async with state.proxy() as data:
        data['pin'] = message.text
    await Pin.new.set()


@dp.callback_query_handler(state=Pin.new, text="savepin", admins_type=True)
async def save_pin(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pin = data['pin']
        try:
            msg = await query.message.answer(await format_pin_text(pin))
            await msg.reply("Новый закреп.")
            new_pin_text(pin)
        except KeyError as e:
            await query.message.answer(f"Вы ввели неправильное сокращения для динамического закрепа - {{{str(e)[1:-1]}}}")
            await state.finish()
            return

    await query.answer("Сохранено")
    await query.message.delete()
    await state.finish()


@dp.callback_query_handler(state=Pin.new, text="unsavepin", admins_type=True)
async def unsave_pin(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Закреп останется прежним.")
    await state.finish()


@dp.message_handler(state=Pin.new, admins_type=True)
async def unsave_pin(message: types.Message, state: FSMContext):
    await message.answer("Закреп останется прежним.")
    await state.finish()


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
    await query.message.edit_text(payload.add_qiwis_text)
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
            api_accs = await api.get_balance()
            balance = api_accs[0].balance
            last_transactions = await api.get_transactions(rows=20)
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


@dp.message_handler(commands=['alert', 'alerts'], admins_type=True)
async def alert_command(message: types.Message):
    await message.answer(payload.alert_text, reply_markup=alert_keyboard)


# alert bot
@dp.callback_query_handler(text="alert_bot", admins_type=True)
async def alert_bot(query: types.CallbackQuery):
    await query.message.edit_text(payload.make_alert_text.format(bot_type="Основного бота"))
    await Alert.bot.set()


@dp.message_handler(state=Alert.bot, admins_type=True)
async def text_alert_bot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer(
        payload.alert_accept_text.format(text=message.text),
        reply_markup=alert_accept_keyboard
    )
    await Alert.bot_accept.set()


@dp.callback_query_handler(text="alert_edit", state=Alert.bot_accept, admins_type=True)
async def alert_edit(query: types.CallbackQuery):
    await query.message.edit_text(payload.edit_alert_text.format(bot_type="Основного бота"))
    await Alert.bot.set()


@dp.callback_query_handler(text="alert_accept", state=Alert.bot_accept, admins_type=True)
async def alert_accepted(query: types.CallbackQuery, state: FSMContext):
    workers = Worker.select()
    len_users = workers.count()
    msg_count = 0
    blocked_count = 0
    not_found_count = 0

    for worker in workers:
        try:
            async with state.proxy() as data:
                await dp.bot.send_message(worker.cid, data['text'])
            await query.message.edit_text(payload.alert_start_text.format(
                len_users=len_users,
                msg_count=msg_count,
                blocked_count=blocked_count,
                not_found_count=not_found_count,
            ))
            msg_count += 1
        except ChatNotFound:
            not_fount_count += 1
        except BotBlocked:
            blocked_count += 1
        await sleep(0.2)

    await query.message.edit_text(payload.alert_start_text.format(
        len_users=len_users,
        msg_count=msg_count,
        blocked_count=blocked_count,
        not_found_count=not_found_count,
    ))
    await query.message.reply(payload.alert_complete_text)

    await state.finish()

# alert casino


@dp.callback_query_handler(text="alert_casino", admins_type=True)
async def alert_casino(query: types.CallbackQuery):
    await query.message.edit_text(payload.make_alert_text.format(bot_type="Казино ботов"))
    await Alert.casino.set()


@dp.message_handler(state=Alert.casino, admins_type=True)
async def text_alert_casino(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer(
        payload.alert_accept_text.format(text=message.text),
        reply_markup=alert_accept_keyboard
    )
    await Alert.casino_accept.set()


@dp.callback_query_handler(text="alert_edit", state=Alert.casino_accept, admins_type=True)
async def alert_edit(query: types.CallbackQuery):
    await query.message.edit_text(payload.edit_alert_text.format(bot_type="Казиков"))
    await Alert.casino.set()


@dp.callback_query_handler(text="alert_accept", state=Alert.casino_accept, admins_type=True)
async def alert_accepted(query: types.CallbackQuery, state: FSMContext):
    users = CasinoUser.select()
    len_users = users.count()
    msg_count = 0
    blocked_count = 0
    not_found_count = 0

    for user in users:
        try:
            async with state.proxy() as data:
                await casino_bot.send_message(user.cid, data['text'])
            await query.message.edit_text(payload.alert_start_text.format(
                len_users=len_users,
                msg_count=msg_count,
                blocked_count=blocked_count,
                not_found_count=not_found_count,
            ))
            msg_count += 1
        except ChatNotFound:
            not_fount_count += 1
        except BotBlocked:
            blocked_count += 1
        await sleep(0.2)

    await query.message.edit_text(payload.alert_start_text.format(
        len_users=len_users,
        msg_count=msg_count,
        blocked_count=blocked_count,
        not_found_count=not_found_count,
    ))
    await query.message.reply(payload.alert_complete_text)

    await state.finish()


# alert escort
@dp.callback_query_handler(text="alert_escort", admins_type=True)
async def alert_escort(query: types.CallbackQuery):
    await query.message.edit_text(payload.make_alert_text.format(bot_type="Эскорта"))
    await Alert.escort.set()


@dp.message_handler(state=Alert.escort, admins_type=True)
async def text_alert_escort(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer(
        payload.alert_accept_text.format(text=message.text),
        reply_markup=alert_accept_keyboard
    )
    await Alert.escort_accept.set()


@dp.callback_query_handler(text="alert_edit", state=Alert.escort_accept, admins_type=True)
async def alert_edit(query: types.CallbackQuery):
    await query.message.edit_text(payload.edit_alert_text.format(bot_type="Эскорта"))
    await Alert.escort.set()

# alert trading


@dp.callback_query_handler(text="alert_trading", admins_type=True)
async def alert_trading(query: types.CallbackQuery):
    await query.message.edit_text(payload.make_alert_text.format(bot_type="Трейдинга"))
    await Alert.trading.set()


@dp.message_handler(state=Alert.trading, admins_type=True)
async def text_alert_trading(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer(
        payload.alert_accept_text.format(text=message.text),
        reply_markup=alert_accept_keyboard
    )
    await Alert.trading_accept.set()


@dp.callback_query_handler(text="alert_edit", state=Alert.trading_accept, admins_type=True)
async def alert_edit(query: types.CallbackQuery):
    await query.message.edit_text(payload.edit_alert_text.format(bot_type="Трейдинга"))
    await Alert.trading.set()


# reject all alerts
@dp.callback_query_handler(text="alert_reject", state=[Alert.bot_accept, Alert.casino_accept, Alert.escort_accept, Alert.trading_accept], admins_type=True)
async def alert_reject(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(payload.alert_reject_text)
    await state.finish()
