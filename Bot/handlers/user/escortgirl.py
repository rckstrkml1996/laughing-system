from secrets import token_hex

from aiogram import types
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import quote_html

from models import Worker, EscortGirl, EscortGirlPhoto
from loader import dp
from data.texts import (
    zap_text,
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
    esc_create_girl_keyboard,
    esc_delete_girl_keyboard,
)


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


@dp.callback_query_handler(text="form_esc", state="*", is_worker=True)
async def form_escort(query: types.CallbackQuery, worker: Worker):
    try:
        girl = EscortGirl.get(owner=worker)
    except EscortGirl.DoesNotExist:
        return
    if girl:
        await send_girl_anket(girl, query.message)
        await query.answer("Вот твоя анкета!")
    else:
        await query.answer("НЕИЗВЕСТНАЯ ОШИБКА ПИШИ КОДЕРУ @ukhide!")


@dp.callback_query_handler(text="delete_form_esc", state="*", is_worker=True)
async def delete_form_escort(query: types.CallbackQuery, worker: Worker):
    try:
        girl = EscortGirl.get(owner=worker)
    except EscortGirl.DoesNotExist:
        await query.answer("НЕИЗВЕСТНАЯ ОШИБКА ПИШИ КОДЕРУ!")
        return
    await query.answer("Удаляю..")
    EscortGirlPhoto.delete().where(EscortGirlPhoto.owner == girl).execute()
    girl.delete_instance()
    await query.message.edit_caption(query.message.caption, reply_markup=None)


@dp.callback_query_handler(text="create_form_esc", state="*", is_worker=True)
async def create_escort_form(query: types.CallbackQuery):
    await query.message.edit_text(esc_create_name_text)
    await EscortNewForm.name.set()


@dp.message_handler(commands=["newgirl"], state="*", is_admin=True)
async def admin_create_escort_form(message: types.Message, worker: Worker):
    if worker.status == 7:
        await message.answer(esc_create_name_text)
        await EscortNewForm.name.set()


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
    photo_path = f"../media/esc{token_hex(6)}.jpg"
    await message.photo[-1].download(destination_file=photo_path)
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
    photo_path = f"../media/esc{token_hex(6)}.jpg"
    await message.photo[-1].download(destination_file=photo_path)
    async with state.proxy() as data:
        girl = EscortGirl.get(id=data["girl_id"])
    EscortGirlPhoto.create(owner=girl, saved_path=photo_path, file_id=None)
    await message.reply(esc_create_photos_text, reply_markup=esc_create_girl_keyboard)


@dp.message_handler(regexp="Завершить", state="*")
async def cancel_girls(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("/start")
