from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

from utils.basefunctional import (
    get_escort_girls_text_id,
)  # get_escort_girls_text, get_girl_ids

back_welcome_btn = InlineKeyboardButton(
    emojize("Вернуться :leftwards_arrow_with_hook:"), callback_data="welcome"
)


def girls_choice_keyboard(worker_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    texts_ids = get_escort_girls_text_id(worker_id)  # EscortGirl
    # print(texts_ids)

    for text, girl_id in texts_ids:
        # print(text, girl_id)
        markup.add(InlineKeyboardButton(text, callback_data=f"girl_{girl_id}"))

    markup.add(back_welcome_btn)
    return markup


back_girls_btn = InlineKeyboardButton("Назад", callback_data="girls")


def girl_keyboard(girl_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    about_btn = InlineKeyboardButton("Описание", callback_data=f"about_{girl_id}")
    services_btn = InlineKeyboardButton("Услуги", callback_data=f"services_{girl_id}")

    another_photo_btn = InlineKeyboardButton(
        "Показать другое фото", callback_data=f"newphoto_{girl_id}"
    )

    get_btn = InlineKeyboardButton("Оформить", callback_data=f"get_{girl_id}")

    markup.add(about_btn, services_btn)
    markup.add(another_photo_btn)
    markup.add(get_btn, back_girls_btn)

    return markup


pay_url = "https://qiwi.com/payment/form/99?extra[%27account%27]=+{account}&amountInteger={amount}&amountFraction=0&currency=643&extra[%27comment%27]={comment}&blocked[0]=sum&blocked[1]=account&blocked[2]=comment"


def get_girl_keyboard(
    account: str,
    comment,
    one_amount: int,
    two_amount: int,
    full_amount: int,
    pay_id: int,
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    get_hour_btn = InlineKeyboardButton(
        "Час",
        url=pay_url.format(
            account=account,
            amount=one_amount,
            comment=comment,
        ),
    )
    get_twohour_btn = InlineKeyboardButton(
        "Два часа",
        url=pay_url.format(
            account=account,
            amount=two_amount,
            comment=comment,
        ),
    )
    get_fullhour_btn = InlineKeyboardButton(
        "Ночь",
        url=pay_url.format(
            account=account,
            amount=full_amount,
            comment=comment,
        ),
    )

    check_btn = InlineKeyboardButton(
        "Проверить оплату", callback_data=f"check_{pay_id}"
    )

    markup.add(
        get_hour_btn,
        get_twohour_btn,
        get_fullhour_btn,
    )
    markup.add(check_btn)
    markup.add(back_girls_btn)

    return markup
