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

add_qiwi_text = str(
    "Введите <b>Токен</b>, и <b>По желанию</b> Прокси.\n\n"
    "Пример:\n"
    "<code>f420543a9430065db1264535ff4eb1ae</code>\n"
    "<code>http://user:pass@100.255.3.52:6666</code>"
)

invalid_newqiwi_text = emojize(
    "<b>Допущена ошибка</b> при вводе! :warning:\n"
    "Введите <b>Токен</b> и Прокси <b>(Не обяз.)</b>, пример:\n\n"
    "<code>f420543a9430065db1264535ff4eb1ae</code>\n"
    "<code>http://user:pass@100.255.3.52:6666</code> (По желанию)"
)

valid_newqiwi_text = "<b>Киви успешно добавлен!</b>"

qiwi_action_text = emojize(
    "<b>{going} {currency}</b>, <i>{comment}</i>"
)  # going = "+" + amount or "-" + amount //

qiwi_info_text = emojize(
    "Кошелек: <b><i>+{number}</i></b> :kiwi_fruit:\n"
    "Баланс: <b>{amount} {currency}</b>\n"
    "Сегодня: <i>{incoming} {outgoing}</i>\n"
    "Статус: <b>{status}</b>\n"
    "Прокси: <i>{proxy}</i>\n\n"
    "{qiwi_action_texts}"
)  # proxy_url censored

invalid_proxy_text = emojize(
    "Что-то не так с прокси! Удаляю из кошелька с токеном\n<code>{token}</code>"
)  # token censored
