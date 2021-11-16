from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loguru import logger

from models import CasinoUser, CasinoPayment, Worker
from customutils import datetime_local_now
from loader import config, dp, casino_bot, MinDepositValues
from data import texts
from data.states import CasinoAlert, DeleteAll
from data.keyboards import *
from utils.alert import alert_users
from utils.executional import get_correct_str, get_casino_mamonth_info, get_casino_info
from utils import basefunctional


@dp.message_handler(
    Text(startswith="казик", ignore_case=True), state="*", is_worker=True
)
async def casino_info(message: types.Message, worker: Worker, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logger.debug(f"Cancelling state {current_state} in bot start")
        await state.finish()
    logger.debug(f"Worker [{message.chat.id}] want get casino info")
    await message.answer(
        get_casino_info(worker.uniq_key),
        reply_markup=casino_keyboard(worker.casino_min),
        disable_web_page_preview=True,
    )
    # await CasinoAlert.commands.set() # old deleted from states.py
    logger.debug(f"Worker [{message.chat.id}] get casino info succesfully")


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "casupdateinfo", is_worker=True, state="*"
)
async def update_mamonth_info(query: types.CallbackQuery, worker: Worker):
    mb_id = query.data.split("_")[1]
    try:
        user = CasinoUser.get(id=mb_id)  # can get by str
    except CasinoUser.DoesNotExist:
        logger.debug(
            f":update_info: Mamonth [{mb_id}] that worker [{query.from_user.id}] want see does not exist."
        )
        return
    if user.owner != worker:
        logger.warning(
            f":update_info: Worker [{query.from_user.id}] try get different mamonth!"
        )
        return
    text, markup = get_casino_mamonth_info(user)
    await query.message.edit_text(
        text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "updatefart",
    state="*",
    is_worker=True,
)
async def update_mamonth_fart(query: types.CallbackQuery, worker: Worker):
    mb_id = query.data.split("_")[1]
    try:
        user = CasinoUser.get(id=mb_id)  # can get by str
    except CasinoUser.DoesNotExist:
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
    text, markup = get_casino_mamonth_info(user)
    await query.message.edit_text(
        text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "updatemin",
    state="*",
    is_worker=True,
)
async def update_mamonth_fart(query: types.CallbackQuery, worker: Worker):
    mb_id = query.data.split("_")[1]
    try:
        user = CasinoUser.get(id=mb_id)  # can get by str
    except CasinoUser.DoesNotExist:
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
    text, markup = get_casino_mamonth_info(user)
    await query.message.edit_text(
        text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "updatestopped",
    state="*",
    is_worker=True,
)
async def update_mamonth_fart(query: types.CallbackQuery, worker: Worker):
    mb_id = query.data.split("_")[1]
    try:
        user = CasinoUser.get(id=mb_id)  # can get by str
    except CasinoUser.DoesNotExist:
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
    text, markup = get_casino_mamonth_info(user)
    await query.message.edit_text(
        text,
        reply_markup=markup,
    )


def format_mamont(user: CasinoUser) -> str:
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
    lambda cb: cb.data.split("_")[0] == "casupdatemamonths", state="*", is_worker=True
)
async def update_cas_mamonths(query: types.CallbackQuery, worker: Worker):
    page = int(query.data.split("_")[1])
    visible = basefunctional.get_visible_mamonths_casino(worker)
    count = visible.count()
    if count == 0:
        await query.message.edit_text(texts.no_mamonths_text)
    else:
        all_mamonths = "\n".join(
            map(
                lambda v: texts.cas_mamonth_info_text.format(
                    mid=v.id,
                    cid=v.cid,
                    name=v.fullname,
                    balance=v.balance,
                    fortune=v.fort_chance,
                ),
                visible.limit(20),
            )
        )
        await query.message.edit_text(
            texts.all_cas_mamonths_text.format(
                mamonths_plur=get_correct_str(count, "мамонт", "мамонта", "мамонтов"),
                all_mamonths=all_mamonths,
                time=datetime_local_now().strftime("%H:%M:%S"),
            ),
            reply_markup=casino_mamonths_keyboard(count, page, 20),
        )


@dp.callback_query_handler(text="casmamonths", state="*", is_worker=True)
async def cas_mamonths(query: types.CallbackQuery, worker: Worker):
    visible = basefunctional.get_visible_mamonths_casino(worker)
    count = visible.count()
    if count == 0:
        await query.answer(texts.no_mamonths_alert)
    else:
        all_mamonths = "\n".join(
            map(
                lambda v: texts.cas_mamonth_info_text.format(
                    mid=v.id,
                    cid=v.cid,
                    name=v.fullname,
                    balance=v.balance,
                    fortune=v.fort_chance,
                ),
                visible.limit(20),
            )
        )
        await query.message.edit_text(
            texts.all_cas_mamonths_text.format(
                mamonths_plur=get_correct_str(count, "мамонт", "мамонта", "мамонтов"),
                all_mamonths=all_mamonths,
                time=datetime_local_now().strftime("%H:%M:%S"),
            ),
            reply_markup=casino_mamonths_keyboard(count, 1, 20),
        )


@dp.callback_query_handler(text="all_alert_cas", state="*", is_worker=True)
async def cas_mamonths_alert(query: types.CallbackQuery):
    await query.message.answer_photo(
        config.html_style_url,
        caption=texts.cas_alert_text.format(
            casino_sup_username=config.casino_sup_username,
            escort_sup_username=config.escort_sup_username,
            trading_sup_username=config.trading_sup_username,
        ),
    )
    await CasinoAlert.alert.set()


@dp.message_handler(state=CasinoAlert.alert)  # is_worker=True
async def cas_mamonths_alert_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    await message.answer(message.text, reply_markup=serv_alaccept_keyboard)
    await CasinoAlert.alert_true.set()


@dp.callback_query_handler(
    text="alert_accept", state=CasinoAlert.alert_true, is_worker=True
)
async def cas_alert_true(query: types.CallbackQuery, worker: Worker, state: FSMContext):
    # print(alert_users([[1, 2]], casino_bot))
    # worker = Worker.get(cid=query.from_user.id)
    async with state.proxy() as data:
        text = data["text"]
    await state.finish()
    msg_len = worker.cas_users.count()
    async for answer in alert_users(
        text, map(lambda usr: usr.cid, worker.cas_users), casino_bot
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
    lambda cb: cb.data.split("_")[0] == "casadd", is_worker=True, state="*"
)
async def accept_pay(query: types.CallbackQuery):
    pay_id = query.data.split("_")[1]
    try:
        pay = CasinoPayment.get(id=pay_id)
        if pay.done == 1:
            await query.message.edit_text("Мамонт уже оплатил заявку!")
            return

        pay.done = 2
        pay.save()

        await query.message.edit_text(
            query.message.parse_entities() + "\n\nВы приняли заявку"
        )
        logger.debug("Pay accepted.")
        await query.answer("Принял!")
    except CasinoPayment.DoesNotExist:
        await query.answer("Ошибка, Платежа нету!")


@dp.callback_query_handler(text="mindep_cas", state="*", is_worker=True)
async def minimal_deposit_casino(query: types.CallbackQuery, worker: Worker):
    try:
        index = MinDepositValues.index(worker.casino_min) + 1
    except ValueError:
        index = 0
    if index > len(MinDepositValues) - 1:
        index = 0
    worker.casino_min = MinDepositValues[index]
    worker.save()
    await query.message.edit_text(
        get_casino_info(worker.uniq_key),
        reply_markup=casino_keyboard(worker.casino_min),
        disable_web_page_preview=True,
    )
    logger.debug(f"Worker [{worker.cid}] update min casino deposit succesfully")
    await query.answer("Изменил!")


@dp.callback_query_handler(text="delete_all_cas", is_worker=True, state="*")
async def delete_all_cas(query: types.CallbackQuery):
    await DeleteAll.main.set()
    await query.message.answer(
        "Ты уверен, что хочешь скрыть мамонтов?", reply_markup=sure_cas_keyboard
    )


@dp.callback_query_handler(text="unsure", state=DeleteAll.main)
async def unsure_delete_all_cas(query: types.CallbackQuery, state: FSMContext):
    await query.answer("Отменено!")
    await query.message.delete()
    await state.finish()


@dp.callback_query_handler(text="sure", state=DeleteAll.main, is_worker=True)
async def sure_delete_all_cas(
    query: types.CallbackQuery, worker: Worker, state: FSMContext
):
    CasinoUser.update(visible=False).where(CasinoUser.owner == worker).execute()
    await query.message.edit_text("Скрыл!")
    await state.finish()
