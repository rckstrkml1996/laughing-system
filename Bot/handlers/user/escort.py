from asyncio import sleep
from secrets import token_hex

from aiogram import types
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import quote_html
from loguru import logger

from customutils.models import Worker, EscortUser, EscortGirl, EscortGirlPhoto
from customutils.datefunc import datetime_local_now

from loader import dp
from data.payload import (
    zap_text,
    escort_text,
    esc_mamonth_info_text,
    no_mamonths_text,
    all_esc_mamonths_text,
    esc_create_name_text,
    esc_create_about_text,
    esc_create_services_text,
    inv_esc_create_age_text,
    esc_create_age_text,
    inv_esc_create_price_text,
    esc_create_price_text,
    esc_created_text,
    esc_create_photo_text,
    esc_create_photos_text,
)
from data.states import EscortNewForm
from data.keyboards import (
    menu_keyboard,
    escort_keyboard,
    escort_mamonths_keyboard,
    esc_create_girl_keyboard,
    esc_delete_girl_keyboard,
)
from utils.executional import get_correct_str


async def send_girl_anket(girl: EscortGirl, message: types.Message):
    caption = esc_created_text.format(
        one_hour_price=girl.price,
        two_hours_price=girl.two_price,
        night_price=girl.three_price,
        name=girl.name,
        age=girl.age,
        about=girl.about,
        services=girl.services,
    )

    await message.answer_photo(
        InputFile(girl.photos[0].saved_path),
        caption=caption,
        reply_markup=esc_delete_girl_keyboard,
    )

    # if photo_count == 1:
    # elif photo_count > 1:
    #     media = types.MediaGroup()
    #     for photo in girl.photos:
    #         media.attach_photo(InputFile(photo.saved_path), caption)
    #         caption = None

    #     await message.answer_media_group(media, reply_markup=esc_delete_girl_keyboard)


@dp.message_handler(text=emojize("Эскорт :green_heart:"), is_worker=True, state="*")
async def casino_info(message: types.Message, worker: Worker):
    girl_created = worker.escort_girls.count() >= 1

    await message.answer(
        escort_text.format(
            worker_id=worker.uniq_key,
        ),
        reply_markup=escort_keyboard(girl_created),
        disable_web_page_preview=True,
    )


@dp.callback_query_handler(text="form_esc", state="*", is_worker=True)
async def form_escort(query: types.CallbackQuery, worker: Worker):
    try:
        girl = worker.escort_girls.get()
    except EscortGirl.DoesNotExist:
        await query.answer("НЕИЗВЕСТНАЯ ОШИБКА ПИШИ КОДЕРУ!")
        return

    await send_girl_anket(girl, query.message)
    await query.answer("Вот твоя анкета!")


@dp.callback_query_handler(text="delete_form_esc", state="*", is_worker=True)
async def delete_form_escort(query: types.CallbackQuery, worker: Worker):
    await query.answer("Удаляю..")

    try:
        girl = worker.escort_girls.get()
    except EscortGirl.DoesNotExist:
        await query.answer("НЕИЗВЕСТНАЯ ОШИБКА ПИШИ КОДЕРУ!")
        return

    EscortGirlPhoto.delete().where(EscortGirlPhoto.owner == girl).execute()
    girl.delete_instance()

    await query.message.edit_caption(query.message.caption, reply_markup=None)


# start escort new girl

"""

name = State()
about = State()
services = State()
age = State()
price = State()

"""


@dp.message_handler(commands=["newgirl"], state="*", is_admin=True)
async def admin_create_escort_form(message: types.Message, worker: Worker):
    if worker.status == 7:
        await message.answer(esc_create_name_text)
        await EscortNewForm.name.set()


@dp.callback_query_handler(text="create_form_esc", state="*", is_worker=True)
async def create_form_escort(query: types.CallbackQuery, worker: Worker):
    if worker.escort_girls.count() == 0:
        await query.message.answer(esc_create_name_text)
        await EscortNewForm.name.set()
    else:
        await query.answer("Кодеру напиши пж!")


@dp.message_handler(state=EscortNewForm.name)
async def create_form_escort_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = quote_html(message.text)

    await EscortNewForm.next()
    await message.reply(esc_create_about_text)


@dp.message_handler(state=EscortNewForm.about)
async def create_form_escort_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["about"] = quote_html(message.text)

    await EscortNewForm.next()
    await message.reply(esc_create_services_text)


@dp.message_handler(state=EscortNewForm.services)
async def create_form_escort_services(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["services"] = quote_html(message.text)

    await EscortNewForm.next()
    await message.reply(esc_create_age_text)


@dp.message_handler(lambda msg: not msg.text.isdigit(), state=EscortNewForm.age)
async def inv_create_form_escort_age(message: types.Message):
    await message.reply(inv_esc_create_age_text)


@dp.message_handler(state=EscortNewForm.age)
async def create_form_escort_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["age"] = int(message.text)

    await EscortNewForm.next()
    await message.reply(esc_create_price_text)


@dp.message_handler(lambda msg: not msg.text.isdigit(), state=EscortNewForm.price)
async def inv_create_form_escort_price(message: types.Message):
    await message.reply(inv_esc_create_price_text)


@dp.message_handler(state=EscortNewForm.price)
async def create_form_escort_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["price"] = int(message.text)

    await EscortNewForm.next()
    await message.reply(esc_create_photo_text)


@dp.message_handler(state=EscortNewForm.photo)
async def inv_create_form_escort_photo(message: types.Message):
    await message.reply(esc_create_photo_text)


@dp.message_handler(state=EscortNewForm.photo, content_types=["photo"], is_worker=True)
async def inv_create_form_escort_photo(
    message: types.Message, worker: Worker, state: FSMContext
):
    photo_path = f"media/esc{token_hex(6)}.jpg"
    await message.photo[-1].download(photo_path)

    # await message.answer_photo(InputFile(photo_path))

    async with state.proxy() as data:
        girl = EscortGirl.create(  # ADD owner!!
            owner=worker,
            name=data["name"],
            about=data["about"],
            services=data["services"],
            age=data["age"],
            price=data["price"],
            for_all=worker.status == 7,  # DungeonMaster
        )
        data["girl_id"] = girl.id

        EscortGirlPhoto.create(owner=girl, saved_path=photo_path, file_id=None)

    await EscortNewForm.next()
    await message.reply(esc_create_photos_text, reply_markup=esc_create_girl_keyboard)


@dp.message_handler(state=EscortNewForm.photos)
async def inv_create_form_escort_photo(message: types.Message, state: FSMContext):
    await message.reply(zap_text, reply_markup=menu_keyboard)

    async with state.proxy() as data:
        try:
            girl = EscortGirl.get(id=data["girl_id"])
            await send_girl_anket(girl, message)
        except EscortGirl.DoesNotExist:
            await message.answer("НЕИЗВЕСТНАЯ ОШИБКА ПИШИ КОДЕРУ!")

    await state.finish()


@dp.message_handler(state=EscortNewForm.photos, content_types=["photo"])
async def inv_create_form_escort_photo(message: types.Message, state: FSMContext):
    photo_path = f"media/esc{token_hex(6)}.jpg"
    await message.photo[-1].download(photo_path)

    async with state.proxy() as data:
        girl = EscortGirl.get(id=data["girl_id"])

    EscortGirlPhoto.create(owner=girl, saved_path=photo_path, file_id=None)

    await message.reply(esc_create_photos_text, reply_markup=esc_create_girl_keyboard)


@dp.message_handler(regexp="Завершить", state="*")
async def cancel_girls(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("/start")


# end escort new girl


def format_mamont(user: EscortUser) -> str:
    return esc_mamonth_info_text.format(
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
        await query.message.answer(no_mamonths_text)
    else:
        mamonths = worker.esc_users[page * row_width - row_width : page * row_width]
        if not mamonths:
            await query.message.answer(no_mamonths_text)
            logger.debug(f"[{query.from_user.id}] - has no mamonths")
            return

        mamonths_text = "\n".join(map(format_mamont, mamonths))

        data = {
            "text": all_esc_mamonths_text.format(
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
