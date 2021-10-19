from asyncio import sleep
from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from loguru import logger

from customutils.models import Worker, EscortUser, EscortGirl
from customutils.datefunc import datetime_local_now
from data import keyboards
from loader import dp
from data import payload
from data.states import EscortNewForm
from data.keyboards import *
from utils.executional import get_correct_str
from .panel import worker_welcome


@dp.message_handler(regexp="эскорт", is_worker=True, state="*")
async def casino_info(message: types.Message):
    worker = Worker.get(cid=message.from_user.id)
    await message.answer(
        payload.escort_text.format(
            worker_id=worker.uniq_key,
        ),
        reply_markup=escort_keyboard,
        disable_web_page_preview=True,
    )


def format_mamont(user: EscortUser) -> str:
    return payload.esc_mamonth_info_text.format(
        mid=user.id,
        cid=user.cid,
        name=user.fullname,
        balance=user.balance,
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "escupdatemamonths", state="*", is_worker=True
)
async def all_mamonths_command(query: types.CallbackQuery):
    q_page = int(query.data.split("_")[1])
    page = q_page if q_page != 0 else 1

    row_width = 20

    worker = Worker.get(cid=query.from_user.id)
    mamonths_count = worker.esc_users.count()
    localnow = datetime_local_now()
    timenow = localnow.strftime("%H:%M, %S Сек.")

    if mamonths_count == 0:
        await query.message.answer(payload.no_mamonths_text)
    else:
        mamonths = worker.esc_users[page * row_width - row_width : page * row_width]
        if not mamonths:
            await query.message.answer(payload.no_mamonths_text)
            logger.debug(f"[{query.from_user.id}] - has no mamonths")
            return

        mamonths_text = "\n".join(map(format_mamont, mamonths))

        data = {
            "text": payload.all_esc_mamonths_text.format(
                mamonths_plur=get_correct_str(
                    mamonths_count, "Мамонт", "Мамонта", "Мамонтов"
                ),
                all_mamonths=mamonths_text,
                time=timenow,
            ),
            "reply_markup": escort_mamonths_keyboard(
                mamonths_count, page=page, row_width=row_width
            ),
        }

        if q_page == 0:
            await query.message.answer(**data)
            await sleep(0.25)  # some random
            await query.answer("Лови!")
        else:
            await query.message.edit_text(**data)
        logger.debug("Got mamonths list.")


# @dp.callback_query_handler(text="create_form_esc", state="*", is_worker=True)
# async def create_girl_name(query: types.CallbackQuery):
#     await query.message.answer(payload.escort_new_name)
#     await EscortNewForm.name.set()


# @dp.message_handler(state=EscortNewForm.name, is_worker=True)
# async def create_girl_desc(message: types.Message, state: FSMContext):
#     print("asd")
#     async with state.proxy() as data:
#         data["girl_name"] = message.text.replace(";", " ")
#     await message.answer(payload.escort_new_description)
#     await EscortNewForm.description.set()


# @dp.message_handler(state=EscortNewForm.description, is_worker=True)
# async def create_girl_service(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["girl_description"] = message.text.replace(";", " ")
#     await message.answer(payload.escort_new_service)
#     await EscortNewForm.service.set()


# @dp.message_handler(state=EscortNewForm.service, is_worker=True)
# async def create_girl_age(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["girl_service"] = message.text.replace(";", " ")
#     await message.answer(payload.escort_new_age)
#     await EscortNewForm.age.set()


# @dp.message_handler(state=EscortNewForm.age, is_worker=True)
# async def create_girl_price(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["girl_age"] = message.text.replace(";", " ")
#     await message.answer(payload.escort_new_price)
#     await EscortNewForm.price.set()


# @dp.message_handler(state=EscortNewForm.price, is_worker=True)
# async def create_girl_photo(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["girl_price"] = message.text.replace(";", " ")
#     await message.answer(payload.escort_new_photos)
#     await EscortNewForm.photos.set()


# @dp.message_handler(content_types=["photo"], state=EscortNewForm.photos)
# async def create_girl_end(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["girl_photo"] = message.photo[-1].file_id
#     await message.answer(
#         payload.escort_new_photo_added, reply_markup=keyboards.escort_form_keyboard
#     )
#     await state.finish()


# @dp.message_handler(regexp="Создать", is_worker=True)
# async def create_form(message: types.Message):
#     girl = EscortGirl.create()


# @dp.message_handler(regexp="наза", is_worker=True)
# async def back_menu(message: types.Message):
#     await worker_welcome(message)
