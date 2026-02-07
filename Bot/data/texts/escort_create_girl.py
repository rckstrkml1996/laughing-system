from aiogram.utils.emoji import emojize


preformated = emojize("{text}\n\nПример :point_down:\n<code>{example}</code>")

esc_create_name_text = preformated.format(
    text=emojize(":sunglasses: Отправь мне <b>имя</b> для твоей девочки"),
    example="Настя",
)

esc_create_about_text = preformated.format(
    text=emojize(":shushing_face: Отправь мне <b>описание</b> для твоей девочки"),
    example=emojize("Молодая, Красивая, (БЕЗ СПИДА!) :green_heart:"),
)

esc_create_services_text = preformated.format(
    text=emojize(":eye: Отправь мне описание <b>услуг</b> для твоей девочки"),
    example=emojize("Сосу как пылесос, улетаешь в космос :rocket:"),
)

inv_esc_create_age_text = preformated.format(
    text=emojize(
        ":green_apple: Введи числом!!\nОтправь мне <b>возраст</b> для твоей девочки!"
    ),
    example="21",
)

esc_create_age_text = preformated.format(
    text=emojize(":green_apple: Отправь мне <b>возраст</b> для твоей девочки, числом!"),
    example="23",
)

inv_esc_create_price_text = preformated.format(
    text=emojize(
        ":money_with_wings: Введи числом!!\nОтправь мне <b>стоимость</b> для твоей девочки на 1 час!"
    ),
    example="1500",
)

esc_create_price_text = preformated.format(
    text=emojize(
        ":money_with_wings: Отправь мне <b>стоимость</b> для твоей девочки на 1 час, числом!"
    ),
    example="1650",
)

esc_create_photo_text = emojize(
    ':camera: Отправь <b>фотографию</b> для анкеты, нажав "<i>Сжать изображение</i>"'
)

esc_create_photos_text = emojize(
    ":camera: Хочешь добавить <b>еще фоток</b> к анкете?\n"
    'Отправь фотографию для анкеты, нажав "<i>Сжать изображение</i>"'
)

esc_created_text = emojize(
    "Твоя <b>анкета</b> для эскорта :green_heart:\n\n"
    "1 Час: <b>{one_hour_price} RUB</b>\n"
    "2 Час: <b>{two_hours_price} RUB</b>\n"
    "Вся ночь: <b>{night_price} RUB</b>\n\n"
    "Имя: <b>{name}</b>\n"
    "Возраст: <b>{age} годиков</b>\n\n"
    "Описание анкеты:\n<code>{about}</code>\n\n"
    "Описание услуг:\n<code>{services}</code>"
)
