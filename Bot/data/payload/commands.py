from aiogram.utils.emoji import emojize


# worker commands
btc_text = emojize(
    ":money_with_wings: <b>Актуальный</b> курс BTC - {usd} $ (~ {rub} ₽)"
)


help_text = emojize(
    ":woman_tipping_hand: <b>Команды</b> конфы\n"
    "/clc <code>[выражение]</code> - Посчитать на калькуляторе\n"
    "/lzt <code>[ник на LZT]</code> - Найти профить лолза\n"
    "/hash <code>[хэш]</code> - Инфо о BTC хэше\n"
    "/btc <code>[адрес]</code> - Инфо о BTC адресе\n"
    "/help - Показать список команд\n"
    "/me - Показать инфо о себе\n"
    "/btc - Курс биткоина"
)

me_text = emojize(
    ":woman_tipping_hand: Воркер <a href='tg://user?id={cid}'>{username}</a>\n"
    "Telegram ID: {cid}\n\n"
    "{len_profits} профитов на сумму {sum_profits} ₽\n"
    "Средний профит ~ {middle_profits} ₽\n\n"
    "В команде {in_team}, {warns}"
)

lzt_text = emojize(
    "LZT <a href='{permalink}'>{username}</a>\n"
    "Статус: {user_title}\n"
    "Регистрация: {reg_date}\n"
    "Активность: {last_seen_date}\n"
    "{message_count}, {like_count} симп"
)

lolz_down_text = "Задержка запроса, скорей всего LOLZ упал :("

cck_size_text = "Мой размер чилена - {size}см {smile}"


# admins commands
adm_work_command = emojize(
    "<b>Состояние</b> сервисов:\n"
    "{services_status}"
)

setwork_text = emojize(":white_check_mark: <b>Поставлен</b> ворк")
setdontwork_text = emojize(":x: <b>Поставлен</b> неворк")

qiwi_command_text = emojize(
    "Команда киви епта"
)
