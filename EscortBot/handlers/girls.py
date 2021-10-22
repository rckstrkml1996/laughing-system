from random import randint

from aiogram.types import CallbackQuery, InputFile
from loguru import logger

from customutils.qiwiapi import get_api
from customutils.models import EscortUser

from loader import dp, main_bot
from config import config
from data.payload import girls_choice_text, girl_text, girl_get_text
from data.keyboards import girls_choice_keyboard, girl_keyboard, get_girl_keyboard
from utils.executional import (
    get_escort_girl_count,
    get_girl,
    create_payment,
)


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "about")
async def girl_about(query: CallbackQuery):
    girl_id = query.data.split("_")[1]

    girl = get_girl(girl_id)
    if girl is None:
        await query.answer("Ошибка!")
        return

    await query.answer(girl.about, show_alert=True)


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "services")
async def girl_services(query: CallbackQuery):
    girl_id = query.data.split("_")[1]

    girl = get_girl(girl_id)
    if girl is None:
        await query.answer("Ошибка!")
        return

    await query.answer(girl.services, show_alert=True)


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "newphoto")
async def girl_newphoto(query: CallbackQuery):
    girl_id = query.data.split("_")[1]

    girl = get_girl(girl_id)
    if girl is None:
        await query.answer("Ошибка!")
        return

    from random import choice

    girl_photo = choice(girl.photos)
    photo = (
        girl_photo.file_id
        if girl_photo.file_id
        else InputFile(f"../Bot/{girl_photo.saved_path}")
    )
    logger.info(f"in girl_newphoto func {photo=}")

    await query.message.delete()
    msg = await query.message.answer_photo(
        photo,
        girl_text.format(
            name=girl.name,
            hour_price=girl.price,
            two_hours_price=girl.two_price,
            night_price=girl.three_price,
        ),
        reply_markup=girl_keyboard(girl.id),
    )
    
    girl_photo.file_id = msg.photo[-1].file_id  # save as file id
    girl_photo.save()


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "get")
async def girl_get(query: CallbackQuery, user: EscortUser):
    girl_id = query.data.split("_")[1]

    girl = get_girl(girl_id)
    if girl is None:
        await query.answer("Ошибка!")
        return

    try:
        token = config("qiwi_tokens")
        if isinstance(token, list):
            token = token[0]
    except NoOptionError:
        logger.info("ESCORT NO Qiwi Tokens in config!")
        await main_bot.send_message(config("admins_chat"), "Escort girl NoOptionError")
        return

    api, proxy_url = get_api(token)

    try:  # getting qiwi account
        profile = await api.get_profile()
        account = profile.contractInfo.contractId
    except (InvalidToken, InvalidAccount) as ex:  # than change as notify
        logger.warning(f"Invalid Token or Account! {ex}")
        await main_bot.send_message(config("admins_chat"), f"Invalid qiwi? {ex}")
    finally:
        await api.close()

    comment = randint(11111111, 99999999)

    payment = create_payment(user, girl.price, comment)

    await query.message.edit_caption(
        girl_get_text.format(
            name=girl.name,
            hour_price=girl.price,
            two_hours_price=girl.two_price,
            night_price=girl.three_price,
            account=account,
            comment=comment,
        ),
        reply_markup=get_girl_keyboard(
            account,
            comment,
            girl.price,
            girl.two_price,
            girl.three_price,
            payment.id
        ),
    )


@dp.callback_query_handler(text="girls")
async def girls_choice(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer(
        girls_choice_text.format(girls_count=get_escort_girl_count(0)),
        reply_markup=girls_choice_keyboard(0),
    )


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "girl")
async def girl_info(query: CallbackQuery):
    girl_id = query.data.split("_")[1]

    girl = get_girl(girl_id)
    if girl is None:
        await query.answer("Ошибка!")
        return

    girl_photo = girl.photos[0]
    photo = InputFile(f"../Bot/{girl_photo.saved_path}")

    await query.message.delete()  # !!!
    msg = await query.message.answer_photo(
        photo,
        girl_text.format(
            name=girl.name,
            hour_price=girl.price,
            two_hours_price=girl.two_price,
            night_price=girl.three_price,
        ),
        reply_markup=girl_keyboard(girl.id),
    )

    girl_photo.file_id = msg.photo[-1].file_id  # save as file id
    girl_photo.save()
