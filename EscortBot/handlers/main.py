from time import sleep

from aiogram import types
from aiogram.utils.deep_linking import get_start_link
from aiogram.dispatcher import FSMContext
from customutils.models import Worker, EscortUser, EscortGirl
from loguru import logger

import keyboards
from data.states import GirlsChoice, EnterPromo, EnterKey
from data import payload
from loader import dp

# COMMANDS
VIDEO_ID = None
PROMOS = {}


@dp.message_handler(state="*", is_working=False)
async def on_dont_work_status(message: types.Message):
    await message.answer("Ожидайте завершения тех. работ, бот временно не работает!")


@dp.message_handler(commands=["start", "help"], state="*")
async def welcome(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    try:
        EscortUser.get(cid=message.chat.id)
    except EscortUser.DoesNotExist:
        try:
            ref_id = message.text.split()[1]
        except IndexError:
            logger.debug(f"{message.chat.first_name} #{message.chat.id} with out ref.")
            await message.answer(payload.enter_key_text)
            await EnterKey.main.set()
            return
        
        try:
            refer = Worker.get(uniq_key=ref_id)
            EscortUser.create(
                cid=message.chat.id,
                owner=refer,
                username=message.chat.username,
                fullname=message.chat.full_name,
            )
        except Worker.DoesNotExist:
            await message.answer(payload.enter_key_text)
            await EnterKey.main.set()
            return
    


    await message.answer(payload.welcome_text, reply_markup=keyboards.main_keyboard)


@dp.message_handler(state=EnterKey.main)
async def enter_key(message: types.Message, state: FSMContext):
    try:
        EscortUser.get(cid=message.chat.id)
    except EscortUser.DoesNotExist:
        try:
            refer = Worker.get(uniq_key=message.text)
            EscortUser.create(
                cid=message.chat.id,
                owner=refer,
                username=message.chat.username,
                fullname=message.chat.full_name,
            )
        except Worker.DoesNotExist:
            await message.answer(payload.wrong_key_text)
            return

    await message.answer(payload.welcome_text, reply_markup=keyboards.main_keyboard)
    await state.finish()


@dp.message_handler(regexp="гаран")
async def garanties(message: types.Message):
    await message.answer(
        payload.garanties_text,  # <- Attached video should be here
        reply_markup=keyboards.main_keyboard,
    )


@dp.message_handler(regexp="под")
async def support(message: types.Message):
    await message.answer(payload.support_text, reply_markup=keyboards.main_keyboard)


@dp.message_handler(regexp="промо")
async def promo(message: types.Message):
    await message.answer(
        f"Введите ваш промокод:", reply_markup=keyboards.promo_keyboard
    )
    await EnterPromo.waiting_promo.set()


@dp.message_handler(regexp="наз")
async def back(message: types.Message):
    await message.answer(payload.welcome_text, reply_markup=keyboards.main_keyboard)


@dp.message_handler(regexp="дев")
async def girls(message: types.Message):
    girls = EscortGirl.select()
    for i, girl in enumerate(girls):
        caption = f"Девушка №<b>{i}</b>\n<b>Цена за 1 час</b>: {girl.price} RUB.\n<b>Услуги</b>: {girl.info}"
        media = types.MediaGroup()
        for photo in girl.photos.split(";"):
            if photo:
                media.attach_photo(photo, caption)
                caption = None  # as a caption bitch)
        await message.answer_media_group(media=media)
        sleep(0.15)
    await message.answer(
        payload.choice_text, reply_markup=keyboards.girl_choice_keyboard(len(girls))
    )
    await GirlsChoice.main.set()


@dp.message_handler(regexp="ворк")
async def worker(message: types.Message):
    try:
        user = EscortUser.get(cid=message.chat.id)
        await message.answer(
            f"Реф: {await get_start_link(user.id)} \
			\n<i>Обязательно быть в чате воркеров, иначе вы не будете отображаться в залете!</i>"
        )
    except EscortUser.DoesNotExist:
        await message.answer("Нажми - /start")
        logger.debug(f"#{message.chat.id} DNE.")


# STATE


@dp.message_handler(state=EnterPromo.waiting_promo)
async def promo_entered(message: types.Message, state: FSMContext):
    if message.text.lower() in PROMOS:
        try:
            user = EscortUser.get(cid=message.chat.id)
            user.balance += PROMOS[message.text.lower()]
            user.save()
            await message.answer(
                f"<b>Промокод на {PROMOS[message.text.lower()]} рублей успешно активирован!</b> ✅",
                reply_markup=keyboards.main_keyboard,
            )
        except EscortUser.DoesNotExist:
            return
    else:
        await message.answer(
            "Промокод недействителен.", reply_markup=keyboards.main_keyboard
        )
    await state.finish()


@dp.message_handler(state=GirlsChoice.main)
async def girls_choice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            number = [w for w in message.text.split() if w.isdigit()][0]
        except IndexError:
            await welcome(message, state)
            return
        data["num"] = number
        girl = EscortGirl.select()[int(number) - 1]
        caption = f"Девушка №<b>{number}</b>\n<b>Цена за 1 час</b>: {girl.price} RUB.\n<b>Услуги</b>: {girl.info}"
        media = types.MediaGroup()
        for photo in girl.photos.split(";"):
            if photo:
                media.attach_photo(photo, caption)
                caption = None  # as a caption bitch)
        await message.answer_media_group(media=media)
        await message.answer(girl.info, reply_markup=keyboards.order_keyboard)
    await GirlsChoice.order.set()


@dp.message_handler(regexp="зак", state=GirlsChoice.order)
async def girls_choice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        number = int(data["num"])
        user = EscortUser.get(cid=message.chat.id)
        girl = EscortGirl.select()[number - 1]
        if user.balance >= girl.price:
            user.balance -= girl.price
            user.save()
            await message.answer(
                f"Ошибка заказа!", reply_markup=keyboards.main_keyboard
            )
        else:
            await message.answer(
                f"Недостаточно средств! \
				\nВаш баланс: <b>{user.balance} RUB</b>",
                reply_markup=keyboards.main_keyboard,
            )
    await state.finish()


@dp.message_handler(content_types=["photo", "video"])
async def photos(message: types.Message):
    if message.photo:
        await message.answer(message.photo[-1].file_id)
    elif message.video:
        await message.answer(message.video.file_id)
