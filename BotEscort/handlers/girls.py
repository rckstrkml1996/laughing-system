from random import randint, choice

from aiogram.types import CallbackQuery, InputFile
from loguru import logger

from qiwiapi import Qiwi
from qiwiapi.exceptions import InvalidProxy
from models import EscortUser, Worker
from Package.build.lib.models.models import TradingUser
from loader import dp, main_bot, config
from data.texts import girls_choice_text, girl_text, girl_get_text, girl_payed_text
from data.keyboards import (
    girls_choice_keyboard,
    girl_keyboard,
    get_girl_keyboard,
    pay_done_keyboard,
)
from utils import basefunctional


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "about")
async def girl_about(query: CallbackQuery):
    girl_id = query.data.split("_")[1]

    girl = basefunctional.get_girl(girl_id)
    if girl is None:
        await query.answer("Ошибка!")
        return

    await query.answer(girl.about, show_alert=True)


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "services")
async def girl_services(query: CallbackQuery):
    girl_id = query.data.split("_")[1]

    girl = basefunctional.get_girl(girl_id)
    if girl is None:
        await query.answer("Ошибка!")
        return

    await query.answer(girl.services, show_alert=True)


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "newphoto")
async def girl_newphoto(query: CallbackQuery):
    girl_id = query.data.split("_")[1]

    girl = basefunctional.get_girl(girl_id)
    if girl is None:
        await query.answer("Ошибка!")
        return

    girl_photo = choice(girl.photos)
    if girl.photos.count() <= 1:
        await query.answer("Только 1 фотография")  ###
        return

    photo = (
        girl_photo.file_id
        if girl_photo.file_id
        else InputFile(f"../media/{girl_photo.saved_path}")
    )
    logger.debug(f"in girl_newphoto func {photo=}")

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

    girl = basefunctional.get_girl(girl_id)
    if girl is None:
        await query.answer("Ошибка!")
        return

    if isinstance(config.qiwi_tokens, list):
        qiwi = Qiwi(**config.qiwi_tokens[0])
    else:
        await main_bot.send_message(
            config.admins_chat, "Escort girl qiwi_tokens is not list"
        )
        return

    try:  # getting qiwi account
        profile = await qiwi.get_profile()
        account = profile.contractInfo.contractId
    except InvalidProxy as ex:  # than change as notify
        logger.warning(f"Invalid Proxy! {ex}")
        await main_bot.send_message(config.admins_chat, f"Invalid proxy? {ex}")

    comment = randint(11111111, 99999999)

    payment = basefunctional.create_payment(user, girl.price, comment)

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
            account, comment, girl.price, girl.two_price, girl.three_price, payment.id
        ),
    )


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "check")
async def girl_check(query: CallbackQuery):
    pay_id = query.data.split("_")[1]

    payment = basefunctional.get_payment(pay_id)
    if payment is None:
        await query.answer("Платежа нету в базе!", show_alert=True)
        return

    if payment.done == 0:
        await query.answer("Вы ещё не оплатили!")
        return
    elif payment.done == 1:
        time_delta = "1 Час"
    elif payment.done == 2:
        time_delta = "2 Часа"
    elif payment.done == 3:
        time_delta = "Ночь"
    else:
        return

    await query.message.edit_caption(
        girl_payed_text.format(
            time=time_delta, support_username=config.escort_sup_username
        ),
        reply_markup=pay_done_keyboard,
    )


@dp.callback_query_handler(text="girls")
async def girls_choice(query: CallbackQuery):
    worker = EscortUser.get(cid=query.from_user.id).owner

    payload = {
        "text": girls_choice_text.format(
            girls_count=basefunctional.get_escort_girl_count(worker.id)
        ),
        "reply_markup": girls_choice_keyboard(worker.id),
    }

    if query.message.photo:  # without photo
        await query.message.delete()
        await query.message.answer(**payload)
    else:
        await query.message.edit_text(**payload)


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "girl")
async def girl_info(query: CallbackQuery):
    girl_id = query.data.split("_")[1]

    girl = basefunctional.get_girl(girl_id)
    if girl is None:
        await query.answer("Ошибка!")
        return

    girl_photo = girl.photos[0]
    photo = InputFile(girl_photo.saved_path)

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
