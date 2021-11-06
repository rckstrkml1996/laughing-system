from aiogram import types
from aiogram.dispatcher.filters import RegexpCommandsFilter
from aiogram.types import user
from loguru import logger

from models import Worker
from loader import dp, status_names
from data.keyboards import new_status_keyboard
from data.texts import mention_text, set_new_worker_status, worker_choice_one_plz


@dp.message_handler(
    RegexpCommandsFilter(regexp_commands=["nstatus (.+)", "set_status (.+)"]),
    admins_chat=True,
    is_admin=True,
)
async def worker_new_status(message: types.Message, worker: Worker, regexp_command):
    worker_naming = regexp_command.group(1)
    payload = {}

    if worker_naming.isdigit():
        if len(worker_naming) <= 6:
            payload["id"] = int(worker_naming)  # worker id
        else:
            payload["cid"] = int(worker_naming)
    else:
        payload["username"] = worker_naming.replace("@", "")

    try:
        diff_worker = Worker.get(**payload)
    except Worker.DoesNotExist:
        await message.answer("Такого воркера не существует!")
        return

    if diff_worker == worker:
        await message.answer("Ты дурак? Себе самому статус менять??")
        return

    logger.debug(
        f"Change Status: {message.text=} {diff_worker.id=} {diff_worker.status=}"
    )

    await message.answer(
        worker_choice_one_plz.format(
            mention=mention_text.format(user_id=diff_worker.cid, text=diff_worker.name),
            status_len=worker.status,
        ),
        reply_markup=new_status_keyboard(status_names, diff_worker.id, worker.status),
    )


@dp.message_handler(commands=["nstatus", "set_status"], admins_chat=True)
async def inv_worker_new_status(message: types.Message):
    await message.reply("/nstatus 123")


@dp.callback_query_handler(regexp="w([0-9]+)_([0-9]+)", admins_chat=True, is_admin=True)
async def worker_set_status(query: types.CallbackQuery, worker: Worker, regexp):
    diff_worker_id = int(regexp.group(1))  # worket that edit
    status_id = int(regexp.group(2))  # status id

    try:
        diff_worker = Worker.get(id=diff_worker_id)

        status_name = status_names.get_value(status_id)  # status name by id

        logger.debug(f"{diff_worker.status=} {status_name=}")
        diff_worker.status = status_id
        diff_worker.save()  # change in base

        await query.message.edit_text(
            set_new_worker_status.format(
                status_name=status_name,
                mention=mention_text.format(
                    user_id=diff_worker.cid, text=diff_worker.name
                ),
            )
        )
    except Worker.DoesNotExist:
        await query.answer("Какая-то ошибка в коде!")
        logger.debug("worker_set_status dne")
