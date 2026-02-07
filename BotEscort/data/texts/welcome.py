from aiogram.utils.emoji import emojize

# {name} - quote_html
welcome_text = emojize(
    "<b>{name}</b>, добро пожаловать в <b>{bot_name}</b> :green_heart:\n\n"
    "У нас вы можете найти лучших девочек для интимных встреч.\n\n"
    "Выдача адресов происходит круглосуточно через бота или, "
    "в крайних случаях, через куратора!\n\n"
    "Внимательней проверяйте адрес Telegram, "
    "остерегайтесь мошенников, спасибо, "
    "что выбираете нас! :sunglasses:"
)


new_user_text = emojize(
    ":sunglasses: Привет, <b>{name}</b> Введи <b>6-значный код</b> авторизации"
)

new_user_wrong_code_text = emojize(
    ":hankey: Неправильный код, введи ещё раз <b>6-значный</b> код авторизации"
)