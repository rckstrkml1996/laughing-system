from aiogram.utils.emoji import emojize


qiwi_command_text = emojize(
    ":kiwi_fruit: Информация по киви кошелькам.\n\n"
    "Общий баланс: <b>{all_balance} RUB</b>"
)

no_qiwis_text = emojize("У вас нет привязанных кошельков! :x:")


qiwi_to_bot_text = "Введите все необходимые данные <b>мне</b> в лс!"

qiwi_error_text = emojize(
    "Какая-то ошибка в киви, попробуй еще раз или позови кодера) :warning:"
)

wanna_add_qiwi_text = "Введем новый киви?"

add_qiwi_text = emojize(
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

qiwi_info_text = emojize(
    "Кошелек: <b>+{number}</b> :kiwi_fruit:\n"
    "Баланс: <b>{balance}</b>\n"
    "Сумма платежей: <b>+{incoming}</b> <b>-{outgoing}</b>\n"
    "Статус: <b>{status}</b>\n"
    "Прокси: <i>{proxy_url}</i>\n\n"
    "{last_actions}"
)

same_qiwi_text = emojize("Похоже вы пытаетесь добавить такой же киви кошелек)")

qiwi_delete_text = emojize(
    ":wastebasket: Удаляю кошелек с токеном:\n" "<code>{token}</code>"
)

qiwi_selfdelete_text = emojize("Вы уверенны чо хатите удалить этат киви сука? :angry:")

qiwi_add_proxy_text = emojize(
    "Введите <b>HTTP</b> прокси, пример:\n"
    "<code>http://user:pass@100.255.3.52:6666</code>"
)

new_proxy_success_text = emojize(
    "Прокси добавленны для этого кошелька :white_check_mark:"
)

qiwi_proxy_delete = emojize(
    "Удаляю прокси: <i>{proxy}</i>\n"
    "Для кошелька c этим токеном: <code>{token}</code>"
)

proxy_error_text = "Что-то с удалением прокси <b>зови кодера нахуй</b>!!"
