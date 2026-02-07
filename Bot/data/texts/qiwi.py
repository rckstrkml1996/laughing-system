from aiogram.utils.emoji import emojize


qiwi_emoji = emojize(":kiwi_fruit:")  # ? qiwi_emoji_text

qiwi_account_text = "<i>+{number}</i>: <b>{amount} {currency}</b>"

qiwi_tokens_info_text = emojize(
    ":kiwi_fruit: Информация по киви кошелькам.\n\n"
    "{qiwi_account_texts}\n\n"
    "Общий баланс: <b>{all_amounts} RUB</b>"
)

no_qiwis_text = emojize("У вас нет привязанных кошельков! :x:")

qiwi_to_bot_text = "Введите все необходимые данные <b>мне</b> в лс!"

wanna_add_qiwi_text = "Введем новый киви?"

add_qiwi_text = emojize(
    ":rugby_football: Введите <b>Токен</b> <b>Публичный ключ</b>, и <b>По желанию</b> Прокси, пример\n\n"
    "<code>f420543a9430065db1264535ff4eb1ae</code>\n"
    "<code>48e7qUxn9T...P5L49YSCM</code>\n"
    "<code>http://user:pass@100.255.3.52:6666</code>"
)

invalid_newqiwi_text = emojize(
    ":x: <b>Допущена ошибка</b> при вводе!\n"
    "Введите <b>Токен</b> <b>Публичный ключ</b> и Прокси <b>(Не обяз.)</b>, пример:\n\n"
    "<code>f420543a9430065db1264535ff4eb1ae</code>\n"
    "<code>48e7qUxn9T...P5L49YSCM</code>\n"
    "<code>http://user:pass@100.255.3.52:6666</code> (По желанию)"
)

valid_newqiwi_text = "<b>Киви +{number} успешно добавлен!</b>"

qiwi_action_text = emojize(
    "<b>{going} {currency}</b>, <i>{comment}</i>"
)  # going = "+" + amount or "-" + amount //

qiwi_info_text = emojize(
    "Кошелек: <b><i>+{number}</i></b> :kiwi_fruit:\n"
    "Баланс: <b>{amount} {currency}</b>\n"
    "Статус: <b>{status}</b>\n"
    "Прокси: <i>{proxy}</i>\n\n"
    "{qiwi_action_texts}"
)  # proxy_url censored

invalid_proxy_text = emojize(
    "Что-то не так с прокси! Удаляю из кошелька <b>+{number}</b>"
)  # token censored

add_qiwi_cancel_text = "Отменено!"

qiwi_checking_proxy_text = "Проверка прокси [<b>{timeout} сек</b>]"
qiwi_checking_proxy_valid_text = "Прокси <b>валид!</b>"
qiwi_checking_proxy_invalid_text = "Прокси <b>невалид!</b>"
qiwi_invalid_token_text = "<b>Скорей всего неправильный токен!</b>"
qiwi_already_exists_text = emojize(
    ":x: <b>Кошелек с таким токеном уже есть!</b>\n"
    "Введите <b>Токен</b> и Прокси <b>(Не обяз.)</b>, пример:\n\n"
    "<code>f420543a9430065db1264535ff4eb1ae</code>\n"
    "<code>http://user:pass@100.255.3.52:6666</code> (По желанию)"
)
