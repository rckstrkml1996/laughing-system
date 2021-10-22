from aiogram.utils.emoji import emojize


girls_choice_text = emojize(
    ":green_heart: <b>Анкеты наших девочек</b>\n\n"
    ":wave: Свободны сейчас: <b>{girls_count}</b> "
)

girl_text = emojize(
    ":id: Вы выбрали девушку <b>{name}</b>\n\n"
    ":city_sunrise: Час: <b>{hour_price} RUB</b>\n"
    ":cityscape: 2 часа: <b>{two_hours_price} RUB</b>\n"
    ":night_with_stars: Ночь: <b>{night_price} RUB</b>\n\n"
    ":warning: Для оформления нажмите на кнопку <b>Оформить</b>"
)

girl_get_text = emojize(
    ":id: Вы выбрали девушку <b>{name}</b>\n\n"
    ":city_sunrise: Час: <b>{hour_price} RUB</b>\n"
    ":cityscape: 2 часа: <b>{two_hours_price} RUB</b>\n"
    ":night_with_stars: Ночь: <b>{night_price} RUB</b>\n\n"
    "Оплата способом <b><i>Qiwi</i></b>:\n"
    "Номер: <code>+{account}</code>\n"
    "Комментарий: <code>{comment}</code>\n\n"
    ":credit_card: Для оплаты картой нажмите на кнопку ниже и на странице оплаты выберите оплату картой\n\n"
    ":warning: Оплата заказа принимается <b>строго через бота</b>"
)
