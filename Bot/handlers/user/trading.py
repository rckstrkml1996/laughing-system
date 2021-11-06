from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, RegexpCommandsFilter
from loguru import logger

from models import TradingUser, TradingPayment, Worker
from customutils import datetime_local_now
from loader import config, dp, trading_bot, MinDepositValues
from data import texts
from data.states import TradingAlert, ChangeMin
from data.keyboards import *
from utils.alert import alert_users
from utils.executional import (
    get_correct_str,
    get_trading_mamonth_info,
    get_trading_info,
)


@dp.message_handler(
    Text(startswith="трейд", ignore_case=True), state="*", is_worker=True
)
async def trading_info(message: types.Message, worker: Worker, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logger.debug(f"Cancelling state {current_state} in bot start")
        await state.finish()

    logger.debug(f"Worker [{message.chat.id}] want get trading info")

    await message.answer(
        get_trading_info(worker.uniq_key),
        reply_markup=trading_keyboard(worker.trading_min),
        disable_web_page_preview=True,
    )

    # await TradingAlert.commands.set() # old deleted from states.py
    logger.debug(f"Worker [{message.chat.id}] get trading info succesfully")


@dp.message_handler(commands=["trade_min"], state="*", is_worker=True)
async def change_trading_minimal_dep(message: types.Message):
    await message.answer(
        "Введите новою сумму депозита для всех ваших новых мамонтов.\n"
        f"От <b>{config.min_deposit} RUB</b>"
    )
    await ChangeMin.main.set()


@dp.message_handler(
    lambda msg: not msg.text.isdigit(), state=ChangeMin.main, is_worker=True
)
async def invalid_cas_dep_amount(message: types.Message):
    await message.answer(
        f"Сумма должна быть числом от <b>{config.min_deposit} RUB</b>! Введи ещё раз:"
    )


@dp.message_handler(state=ChangeMin.main, is_worker=True)
async def cas_dep_amount(message: types.Message, state: FSMContext, worker: Worker):
    amount = int(message.text)
    if amount >= config.min_deposit:
        worker.trading_min = amount
        worker.save()

        await message.answer(
            f"Теперь для всех твоих новых мамонтов сумма пополнения от <b>{amount} RUB</b>"
        )
        await state.finish()
    else:
        await message.answer(
            f"Сумма слишком маленькая, введи сумму от <b>{config.min_deposit} RUB</b>"
        )


@dp.message_handler(  # ru and en - C word
    RegexpCommandsFilter(regexp_commands=["t(\d+)", "t(\d+)"]),
    state="*",
    is_worker=True,
)
async def trading_command(message: types.Message, worker: Worker, regexp_command):
    mb_id = regexp_command.group(1)
    try:
        user = TradingUser.get(id=mb_id)  # can get by str
    except TradingUser.DoesNotExist:
        await message.reply("Такого мамонта не существует!")
        logger.debug(
            f"Mamonth [{mb_id}] that worker [{message.chat.id}] want see does not exist."
        )
        return

    if user.owner == worker:
        logger.debug(f"/c Worker [{message.chat.id}] get mamonth info.")
    elif user.status >= 4:  # if user support and upper
        logger.debug(
            f"/c Admin:{user.status} [{message.chat.id}] get not self mamonth info"
        )
    else:
        logger.warning(f"/c Worker [{message.chat.id}] try get different mamonth!")
        return

    text, markup = get_trading_mamonth_info(user)

    await message.answer(
        text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "tdgupdateinfo", is_worker=True, state="*"
)
async def update_mamonth_info(query: types.CallbackQuery, worker: Worker):
    mb_id = query.data.split("_")[1]
    try:
        user = TradingUser.get(id=mb_id)  # can get by str
    except TradingUser.DoesNotExist:
        logger.debug(
            f":update_info: Mamonth [{mb_id}] that worker [{query.from_user.id}] want see does not exist."
        )
        return

    if user.owner != worker:
        logger.warning(
            f":update_info: Worker [{query.from_user.id}] try get different mamonth!"
        )
        return

    text, markup = get_trading_mamonth_info(user)

    await query.message.edit_text(
        text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "tdgupdatefart",
    state="*",
    is_worker=True,
)
async def update_mamonth_fart(query: types.CallbackQuery, worker: Worker):
    mb_id = query.data.split("_")[1]
    try:
        user = TradingUser.get(id=mb_id)  # can get by str
    except TradingUser.DoesNotExist:
        logger.debug(
            f"Mamonth [{mb_id}] that worker [{query.from_user.id}] want update fart does not exist."
        )

    if user.owner != worker:
        logger.warning(
            f":update_info: Worker [{query.from_user.id}] try get different mamonth!"
        )
        return

    user.fort_chance = int(  # update fort chance
        100 if user.fort_chance == 0 else 50 if user.fort_chance == 100 else 0
    )
    user.save()

    text, markup = get_trading_mamonth_info(user)

    await query.message.edit_text(
        text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "tdgupdatemin",
    state="*",
    is_worker=True,
)
async def update_mamonth_fart(query: types.CallbackQuery, worker: Worker):
    mb_id = query.data.split("_")[1]
    try:
        user = TradingUser.get(id=mb_id)  # can get by str
    except TradingUser.DoesNotExist:
        logger.debug(
            f"Mamonth [{mb_id}] that worker [{query.from_user.id}] want update fart does not exist."
        )

    if user.owner != worker:
        logger.warning(
            f":update_info: Worker [{query.from_user.id}] try get different mamonth!"
        )
        return

    try:
        index = MinDepositValues.index(user.min_deposit) + 1
    except ValueError:
        index = 0

    if index > len(MinDepositValues) - 1:
        index = 0

    user.min_deposit = MinDepositValues[index]
    user.save()

    text, markup = get_trading_mamonth_info(user)

    await query.message.edit_text(
        text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "tdgupdatestopped",
    state="*",
    is_worker=True,
)
async def update_mamonth_fart(query: types.CallbackQuery, worker: Worker):
    mb_id = query.data.split("_")[1]
    try:
        user = TradingUser.get(id=mb_id)  # can get by str
    except TradingUser.DoesNotExist:
        logger.debug(
            f"Mamonth [{mb_id}] that worker [{query.from_user.id}] want updatestopped does not exist."
        )

    if user.owner != worker:
        logger.warning(
            f":updatestopped: Worker [{query.from_user.id}] try get different mamonth!"
        )
        return

    user.stopped = not user.stopped
    user.save()

    text, markup = get_trading_mamonth_info(user)

    await query.message.edit_text(
        text,
        reply_markup=markup,
    )


def format_mamont(user: TradingUser) -> str:
    return texts.cas_mamonth_info_text.format(
        mid=user.id,
        cid=user.cid,
        name=user.fullname,
        balance=user.balance,
        fortune="Вкл"
        if user.fort_chance == 100
        else "Выкл"
        if user.fort_chance == 0
        else f"{user.fort_chance} %",
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "tdgupdatemamonths", state="*", is_worker=True
)
async def cas_mamonths_info(query: types.CallbackQuery, worker: Worker):
    q_page = int(query.data.split("_")[1])  # raise if shit
    page = q_page if q_page != 0 else 1

    row_width = 20

    # worker = Worker.get(cid=query.from_user.id)
    mamonths_count = worker.cas_users.count()
    localnow = datetime_local_now()
    timenow = localnow.strftime("%H:%M, %S Сек.")
    if mamonths_count == 0:
        await query.message.edit_text(texts.no_mamonths_text)
    else:  # format mamonth its a def on 176 line mb not()
        cusers = list(worker.cas_users)[::-1]
        mamonths = cusers[page * row_width - row_width : page * row_width]
        if not mamonths:
            await query.message.answer(texts.no_mamonths_text)
            return  # logg plz

        mamonths_text = "\n".join(
            map(
                format_mamont,
                mamonths,
            )
        )

        data = {
            "text": texts.all_cas_mamonths_text.format(
                mamonths_plur=get_correct_str(
                    mamonths_count, "Мамонт", "Мамонта", "Мамонтов"
                ),
                all_mamonths=mamonths_text,
                time=timenow,
            ),
            "reply_markup": trading_mamonths_keyboard(
                mamonths_count, page=page, row_width=row_width
            ),
        }

        if q_page == 0:
            await query.message.answer(**data)
            await sleep(0.25)
            await query.answer("Лови!")
        else:
            await query.message.edit_text(**data)

        logger.debug("Got mamonths list.")


@dp.callback_query_handler(text="all_alert_tdg", state="*", is_worker=True)
async def cas_mamonths_alert(query: types.CallbackQuery):
    await query.message.answer_photo(
        config.html_style_url,
        caption=texts.cas_alert_text.format(
            trading_sup_username=config.trading_sup_username,
            escort_sup_username=config.escort_sup_username,
            trading_sup_username=config.trading_sup_username,
        ),
    )
    await TradingAlert.alert.set()


@dp.message_handler(state=TradingAlert.alert)  # is_worker=True
async def cas_mamonths_alert_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await message.answer(message.text, reply_markup=serv_alaccept_keyboard)
    await TradingAlert.alert_true.set()


@dp.callback_query_handler(
    text="alert_accept", state=TradingAlert.alert_true, is_worker=True
)
async def cas_alert_true(query: types.CallbackQuery, worker: Worker, state: FSMContext):
    # print(alert_users([[1, 2]], trading_bot))
    # worker = Worker.get(cid=query.from_user.id)
    async with state.proxy() as data:
        text = data["text"]
    await state.finish()

    msg_len = worker.cas_users.count()
    async for answer in alert_users(
        text, map(lambda usr: usr.cid, worker.cas_users), trading_bot
    ):
        await sleep(0.3)  # delay
        if answer["network_count"] > 0:
            await query.message.edit_text("Телеграмм не отвечает на запрос :(")
            return
        elif answer["cantparse_count"] > 0:
            await query.message.edit_text("Что-то с текстом, не парсит :(")
            return
        elif answer["internal_count"] > 0:
            await query.message.edit_text("Какая-то ошибка в рассылке, сообщи кодеру!")
            return
        else:
            try:
                localnow = datetime_local_now()
                timenow = localnow.strftime("%H:%M, %S cек")
                await query.message.edit_text(
                    texts.cas_alsend_text.format(
                        text=text,
                        msg_count=answer["msg_count"],
                        msg_len=msg_len,
                        timenow=timenow,
                    )
                )
            except Exception as ex:
                logger.exception(ex)

    await query.message.reply("Рассылка завершилась.")
    logger.debug("Alert done.")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "tdgpayaccept", is_worker=True, state="*"
)
async def accept_pay(query: types.CallbackQuery):
    pay_id = query.data.split("_")[1]
    try:
        pay = TradingPayment.get(id=pay_id)
        check_time = config.qiwi_check_time * 2  # - 3 just for somethink)
        exact_time = (datetime_local_now() - pay.created).seconds

        logger.debug(f"{check_time=} (qiwi_check_time * 2), {exact_time=}")

        if pay.done == 1:
            await query.message.edit_text("Мамонт уже оплатил заявку!")
            return
        elif exact_time >= check_time:
            pay.done = 2
            pay.save()
        elif exact_time <= check_time:
            await query.answer(f"Жди еще {check_time - exact_time} секунд!")
            return
        else:
            await query.answer(f"Зови кодера)")
            return

        await query.message.edit_text(
            query.message.parse_entities() + "\n\nВы приняли заявку"
        )
        logger.debug("Pay accepted.")
        await query.answer("Принял!")
    except TradingPayment.DoesNotExist:
        await query.answer("Ошибка!")


@dp.callback_query_handler(text="mindep_tdg", state="*", is_worker=True)
async def minimal_deposit_trading(query: types.CallbackQuery, worker: Worker):
    try:
        index = MinDepositValues.index(worker.trading_min) + 1
    except ValueError:
        index = 0

    if index > len(MinDepositValues) - 1:
        index = 0

    worker.trading_min = MinDepositValues[index]
    worker.save()

    await query.message.edit_text(
        get_trading_info(worker.uniq_key),
        reply_markup=trading_keyboard(worker.trading_min),
        disable_web_page_preview=True,
    )
    logger.debug(f"Worker [{worker.cid}] update min trading deposit succesfully")

    await query.answer("Изменил!")
