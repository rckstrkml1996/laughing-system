from aiogram.utils.emoji import emojize


mamonth_stopped_true = emojize(
    ":x: <b>Мамонту (</b>/c{user_id}<b>) включены Тех. работы!</b>"
)
mamonth_stopped_false = emojize(
    ":white_check_mark: <b>Мамонту (</b>/c{user_id}<b>) выключены Тех. работы!</b>"
)

casino_text = emojize(
    "Казино :slot_machine: [<code>{worker_id}</code>]\n\n"
    "<a href='t.me/{casino_username}'>Бот для работы</a>\n"
    "<a href='t.me/{casino_sup_username}'>Тех. поддержка</a>\n\n"
    "<a href='t.me/{casino_username}?start={worker_id}'>Твоя реферальная ссылка</a>\n\n"
    "🥝 Qiwi с фейк пополнения:\n"
    "{pay_qiwis}\n\n"
    "💳 Карты фейк пополнения:\n"
    "{pay_cards}\n\n"
    "/info [ID Мамонта] - Профиль мамонта\n"
    "/fart [ID Мамонта] - 100/0/50% шанс\n"
    "/msg [ID Мамонта] - Отправить сообщение мамонту\n"
    "/blc [ID Мамонта] - Тех. работы мамонту\n"
    "/casino_min - Изменить общую минималку"
)

casino_msg_text = emojize(":full_moon: <b>Сообщение</b> было отправлено")

no_user_text = emojize(":warning: Нету мамонта с этим ID")
no_mamonth_text = emojize(":warning: У вас нет мамонта с этим ID")
invalid_match_text = emojize(":warning: Неправильно введены данные.")

cas_mamonth_info_text = "(/c{mid}) - <a href='tg://user?id={cid}'>{name}</a> - <b>{balance} RUB</b>, фарт - {fortune}"

balance_changed_text = emojize(
    ":ok_hand: Баланс мамонта /c{user_id} - <b>{amount} RUB</b>"
)

no_mamonths_text = emojize(":slot_machine: <b>У тебя ещё нету мамонтов!</b>")
no_mamonths_alert = emojize(":slot_machine: У тебя ещё нету мамонтов!")

all_cas_mamonths_text = emojize(
    ":slot_machine: У тебя <b>{mamonths_plur}</b>:\n\n"
    "{all_mamonths}\n\n"
    "Обновлено в <i>{time}</i>"
)

casino_mamonth_info = emojize(
    "{smile} Мамонт с ID <b>c{uid}</b>\n\n"
    "Telegram ID: [<code>{chat_id}]</code>\n"
    "ID мамонта: <b>c{uid}</b>\n"
    "Имя: <a href='tg://user?id={chat_id}'>{name}</a>\n\n"
    "Баланс: <b>{balance}</b> ₽\n"
    "Валюта: <b>🇷🇺</b>\n"
    "Фарт: <b>{fortune}</b>\n"
    "Выигрышей: <b>{wins_count}</b>\n"
    "Пополнений: <b>{adds_count}</b>\n"
    "Проигрышей: <b>{lose_count}</b>\n"
    # "Заявок на вывод: <b>0</b>\n"
    "Зачисленных пополнений: <b>{pays_accepted_amount}</b> ₽\n"
    "Всего поднял на казино: <b>{adds_amount}</b> ₽\n\n"
    "Обновлено в <i>{time}</i>"
)

fart_on_text = emojize(":full_moon: <b>Вы</b> включили фарт мамонту {name}")
fart_fif_text = emojize(
    ":full_moon::new_moon: <b>Вы</b> включили/выключили фарт мамонту {name}"
)
fart_off_text = emojize(":new_moon: <b>Вы</b> выключили фарт мамонту {name}")

mamonth_delete_text = emojize(":coffin: <b>Вы</b> удалили мамонта {name}")

cas_alert_text = emojize(
    ":woman_tipping_hand: Массовая рассылка сообщения всем вашим мамонтам\n"
    ":email: Введите сообщение для отправки\n\n"
    "Запрещено использовать любые ТП кроме {casino_sup_username}, {escort_sup_username} и {trading_sup_username}\n"
    "Запрещено принимать оплату на любые реквизиты кроме наших"
)

cas_alsend_text = emojize(
    ":slot_machine: Рассылка была запущена\n"
    ":email: Текст рассылки:\n\n{text}\n\n"
    ":diamond_shape_with_a_dot_inside: Сообщение отправлено: {msg_count} / {msg_len}\n"
    ":arrow_up_small: Обновленно: {timenow}"
)

cas_alsended_text = emojize(
    ":slot_machine: Рассылка закончилась.\n"
    ":email: Текст рассылки:\n{text}\n\n"
    ":diamond_shape_with_a_dot_inside: Сообщение отправлено: {msg_count} / {msg_len}"
)
