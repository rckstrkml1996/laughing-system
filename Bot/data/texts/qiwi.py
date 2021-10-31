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
) # going = "+" + amount or "-" + amount //

qiwi_info_text = emojize(
    "Кошелек: <b><i>+{number}</i></b> :kiwi_fruit:\n"
    "Баланс: <b>{amount} {currency}</b>\n"
    "24 Часа платежи: <i>+{incoming} {currency} -{outgoing} {currency}</i>\n"
    "Статус: <b>{status}</b>\n"
    "Прокси: <i>{proxy_url:.6f}</i>\n\n"
    "{qiwi_action_texts}"
)

# same_qiwi_text = emojize("Похоже вы пытаетесь добавить такой же киви кошелек)")

# qiwi_delete_text = emojize(
#     ":wastebasket: Удаляю кошелек с токеном:\n" "<code>{token}</code>"
# )

# qiwi_selfdelete_text = emojize("Вы уверенны чо хатите удалить этат киви сука? :angry:")

# qiwi_add_proxy_text = emojize(
#     "Введите <b>HTTP</b> прокси, пример:\n"
#     "<code>http://user:pass@100.255.3.52:6666</code>"
# )

# new_proxy_success_text = emojize(
#     "Прокси добавленны для этого кошелька :white_check_mark:"
# )

# qiwi_proxy_delete = emojize(
#     "Удаляю прокси: <i>{proxy}</i>\n"
#     "Для кошелька c этим токеном: <code>{token}</code>"
# )

# proxy_error_text = "Что-то с удалением прокси <b>зови кодера нахуй</b>!!"
