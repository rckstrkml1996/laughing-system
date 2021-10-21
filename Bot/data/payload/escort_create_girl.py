from aiogram.utils.emoji import emojize


preformated = "{text}\n\nПример :point_down:\n<code>{example}</code>"


esc_create_name_text = preformated.format(
    text=emojize(":sunglasses: Отправь мне <b>имя</b> для твоей девочки\n"),
    example="Настя",
)

esc_create_about_text = preformated.format(
    text=emojize(":shushing_face: Отправь мне <b>описание</b> для твоей девочки\n"),
    example=emojize("Молодая, Красивая, (БЕЗ СПИДА!) :green_heart:"),
)

esc_create_services_text = preformated.format(
    text=emojize(":eye: Отправь мне описание <b>услуг</b> для твоей девочки\n"),
    example=emojize("Сосу как пылесос, улетаешь в космос :rocket:"),
)

esc_create_age_text = preformated.format(
    text=emojize(
        ":green_apple: Отправь мне <b>возраст</b> для твоей девочки, числом!\n"
    ),
    example="21",
)

esc_create_price_text = preformated.format(
    text=emojize(
        ":green_apple: Отправь мне <b>стоимость</b> для твоей девочки на 1 час, числом!\n"
    ),
    example="1650",
)


# name = CharField(default="Настя")
# about = CharField(default="Без описания")
# services = CharField(default="Без услуг")
# age = IntegerField(default=20)
# price = IntegerField(default=1500)
