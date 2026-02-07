from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import RegexpCommandsFilter
from loguru import logger

from loader import dp, config, casino_bot
from models import Worker, CasinoUser
from data.states import ChangeMin, SendMessage
from data import texts, keyboards
from utils.executional import get_casino_mamonth_info


@dp.message_handler(
    RegexpCommandsFilter(
        regexp_commands=[
            "bal [cс](\d+)[:;_](\d+)",
            "balance [cс](\d+)[:;_](\d+)",
        ]
    ),
    state="*",
    is_worker=True,
)
async def change_balance(message: types.Message, worker: Worker, regexp_command):
    try:
        user = (
            CasinoUser.select()
            .where(
                CasinoUser.id == int(regexp_command.group(1)),
                CasinoUser.owner == worker,
            )
            .get()
        )
        user.balance = int(regexp_command.group(2))
        user.save()
        await message.answer(
            texts.balance_changed_text.format(
                user_id=user.id,
                amount=user.balance,
            )
        )
    except CasinoUser.DoesNotExist:
        await message.answer(texts.no_mamonth_text)


@dp.message_handler(  # ru and en
    RegexpCommandsFilter(regexp_commands=["fart [cс](\d+)", "fort [cс](\d+)"]),
    state="*",
    is_worker=True,
)
async def fart_command(message: types.Message, worker: Worker, regexp_command):
    mamonth_id = int(regexp_command.group(1))
    try:
        user = CasinoUser.get(id=mamonth_id)
        if user.owner != worker:
            logger.info(f"Worker: {message.chat.id} try get different mamonth!")
            return

        user.fort_chance = (
            100 if user.fort_chance == 0 else 50 if user.fort_chance == 100 else 0
        )
        user.save()
        if user.fort_chance == 0:
            await message.answer(
                texts.fart_off_text.format(
                    name=user.fullname,
                )
            )
        elif user.fort_chance == 50:
            await message.answer(
                texts.fart_fif_text.format(
                    name=user.fullname,
                )
            )
        else:
            await message.answer(
                texts.fart_on_text.format(
                    name=user.fullname,
                )
            )
    except CasinoUser.DoesNotExist:
        await message.reply("Такого мамонта не существует!")


@dp.message_handler(  # ru and en - C word
    RegexpCommandsFilter(regexp_commands=["block c(\d+)", "blk с(\d+)", "blc c(\d+)"]),
    state="*",
    is_worker=True,
)
async def block_command(message: types.Message, worker: Worker, regexp_command):
    user = (
        CasinoUser.select()
        .where(
            CasinoUser.owner == worker, CasinoUser.id == int(regexp_command.group(1))
        )
        .get()
    )
    user.stopped = not user.stopped
    user.save()
    await message.answer(
        texts.mamonth_stopped_true.format(user_id=user.id)
        if user.stopped
        else texts.mamonth_stopped_false.format(user_id=user.id)
    )


@dp.message_handler(  # ru and en - C word
    RegexpCommandsFilter(regexp_commands=["msg c(\d+)", "message с(\d+)"]),
    state="*",
    is_worker=True,
)
async def message_command(message: types.Message, worker: Worker, regexp_command):
    try:
        user = (
            CasinoUser.select()
            .where(
                CasinoUser.owner == worker,
                CasinoUser.id == int(regexp_command.group(1)),
            )
            .get()
        )
        await SendMessage.text.set()
        state = dp.current_state()
        await state.update_data(cid=user.cid)
        await message.answer("Введите текст который отправиться мамонту!")
    except CasinoUser.DoesNotExist:
        await message.answer("DNE")


@dp.message_handler(state=SendMessage.text, is_worker=True)
async def send_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text

    await SendMessage.send.set()
    await message.answer(message.text, reply_markup=keyboards.sure_cas_keyboard)


@dp.callback_query_handler(text="unsure", state=SendMessage.send)
async def send_message_sure(query: types.CallbackQuery, state: FSMContext):
    await query.answer("Отмена!")
    await query.message.delete()
    await state.finish()


@dp.callback_query_handler(text="sure", state=SendMessage.send, is_worker=True)
async def send_message_sure(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await casino_bot.send_message(data["cid"], data["text"])
    await query.message.edit_text(
        query.message.parse_entities() + "\n<b>Отправленно мамонту!</b>"
    )
    await query.answer("Отправил!", show_alert=True)
    await state.finish()


@dp.message_handler(  # ru and en - C word
    RegexpCommandsFilter(regexp_commands=["c(\d+)", "с(\d+)"]),
    state="*",
    is_worker=True,
)
async def casino_command(message: types.Message, worker: Worker, regexp_command):
    mb_id = regexp_command.group(1)
    try:
        user = CasinoUser.get(id=mb_id)  # can get by str
    except CasinoUser.DoesNotExist:
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
    text, markup = get_casino_mamonth_info(user)
    await message.answer(
        text,
        reply_markup=markup,
    )


@dp.message_handler(commands=["casino_min"], state="*", is_worker=True)
async def change_casino_minimal_dep(message: types.Message):
    await message.answer(
        "Введите новою сумму депозита для всех ваших новых мамонтов.\n"
        f"От <b>{config.min_deposit} RUB</b>"
    )
    await ChangeMin.main.set()


@dp.message_handler(state=ChangeMin.main, is_worker=True)
async def cas_dep_amount(message: types.Message, state: FSMContext, worker: Worker):
    amount = int(message.text)
    if amount >= config.min_deposit:
        worker.casino_min = amount
        worker.save()
        await message.answer(
            f"Теперь для всех твоих новых мамонтов сумма пополнения от <b>{amount} RUB</b>"
        )
        await state.finish()
    else:
        await message.answer(
            f"Сумма слишком маленькая, введи сумму от <b>{config.min_deposit} RUB</b>"
        )


@dp.message_handler(
    lambda msg: not msg.text.isdigit(), state=ChangeMin.main, is_worker=True
)
async def invalid_cas_dep_amount(message: types.Message):
    await message.answer(
        f"Сумма должна быть числом от <b>{config.min_deposit} RUB</b>! Введи ещё раз:"
    )
