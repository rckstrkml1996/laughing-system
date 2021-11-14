from aiogram.utils.emoji import emojize


# worker commands
btc_text = emojize(
    ":money_with_wings: <b>Актуальный</b> курс BTC - {usd} $ (~ {rub} ₽)"
)


help_text = emojize(
    ":snake: <b>Команды</b> чата\n\n"
    "/top - Топ за всё время\n"
    "/topm - Топ за месяц\n"
    "/topn - Топ за неделю\n"
    "/topd - Топ за день\n\n"
    "/clc [<code>выражение]</code> - Посчитать на калькуляторе\n"
    "/help - Показать список команд\n"
    "/me - Показать инфо о себе\n"
    "/btc - Курс биткоина"
)

me_text = emojize(
    "{status} - {mention}\n"
    "Telegram ID: {cid}\n\n"
    "<b>{profits}</b> на сумму: <b>{sum_profits} RUB</b>\n"
    "Средний профит: <b>{middle_profits} RUB</b>\n\n"
    "В команде: <b>{in_team}</b>, {warns}"
)

lzt_text = emojize(
    "LZT <a href='{permalink}'>{username}</a>\n"
    "Статус: {user_title}\n"
    "Регистрация: {reg_date}\n"
    "Активность: {last_seen_date}\n"
    "{message_count}, {like_count} симп"
)

lolz_down_text = "Задержка запроса, скорей всего <b>Лолзтим</b> упал :("

cck_size_text = "Размер органа: <b>{size}см</b> {smile}"


# admins commands
adm_work_command = emojize("<b>Состояние</b> сервисов:\n{services_status}")

# work command
setwork_text = emojize("<b>Поставлен</b> ворк :white_check_mark:")
setdontwork_text = emojize("<b>Поставлен</b> неворк :x:")

casino_setwork_text = emojize("Казино - <b>Поставлен</b> ворк :white_check_mark:")
casino_setdontwork_text = emojize("Казино - <b>Поставлен</b> неворк :x:")
escort_setwork_text = emojize("Эскорт - <b>Поставлен</b> ворк :white_check_mark:")
escort_setdontwork_text = emojize("Эскорт - <b>Поставлен</b> неворк :x:")
trading_setwork_text = emojize("Трейдинг - <b>Поставлен</b> ворк :white_check_mark:")
trading_setdontwork_text = emojize("Трейдинг - <b>Поставлен</b> неворк :x:")


alert_text = emojize(
    "Отправка сообщения <b>всем</b> пользователя бота.\n"
    ":face_with_monocle: Выберите бота для оповещений."
)

make_alert_text = emojize(
    "Отправка всем пользователям <b>{bot_type}</b>\n" ":imp: Введите текст:"
)

edit_alert_text = emojize(
    "Отравка всем пользователям <b>{bot_type}</b>\n" ":imp: Введите <b>новый</b> текст:"
)

alert_accept_text = emojize(
    ":thinking_face: Вы уверены что хотите отправить это?\n\n{text}"
)

alert_reject_text = emojize(":wastebasket: Текст <b>не будет</b> отправлен!")

alert_start_text = emojize(
    "Начинаю рассылку всем пользователям.\n"
    "Кол-во пользователей: <b>{len_users}</b>\n\n"
    "Сообщений отправлено: <b>{msg_count}</b>\n"
    "Заблокировали бота: <b>{blocked_count}</b>\n"
    "Не найдено: <b>{not_found_count}</b>\n\n"
    "Обновленно: {timenow}"
)

alert_complete_text = "Рассылка завершилась)"

sys_info_text = emojize(
    ":mechanical_arm: Информация о системе:\n\n"
    "Кол-во ядер: <b>{cpu_count}</b>\n"
    "Кол-во ОЗУ: <b>{ram_count} МБ</b>\n\n"
    "Загруженность ОЗУ: <b>{ram_usage}</b> %\n"
    "Загруженность ЦП: <b>{cpu_usage}</b> %\n\n"
    "Время работы компьютера: <b>{computer_work}</b>"
)

admins_help_text = emojize(
    ":snake: <b>Команды</b> чата\n\n"
    "/sysinfo - Информация о сервере.\n"
    "/pin или /pinned - Действия с закрепленным сообщением.\n"
    "/qiwi - Работа с киви кошельками.\n"
    "/alert - Работа с Оповещениями.\n"
    "/work - Действия с статусом работы проекта.\n"
    "/btc_auth - Проверка Авторизации в аккаунте банкира.\n"
    "/btc_logout - Выйти из аккаунта банкира.\n"
    "/prft, /profit - Создать профит\n"
    "/prftstick - Стикер к профиту\n"
    "/stat - Статистика проекта\n"
    "/card - Изменить карту для прямиков\n"
    "/nstatus [<code>TgID Воркера]</code> - Изменить статус воркера\n"
    "/card - Изменить карту для прямиков\n"
    # "/new_dsgn - Бета хуета ещо нету)\n"
)


ban_success_text = emojize(
    "<b>Успешно забанил</b>: <a href='tg://user?id={cid}'>{name}</a>"
)
kick_success_text = emojize(
    "<b>Успешно кикнул</b>: <a href='tg://user?id={cid}'>{name}</a>"
)

you_banned_text = emojize("<b>Тебя забанили навсегда...</b> :disappointed_relieved:")
you_kicked_text = emojize(
    "<b>Тебя исключили</b> :disappointed_relieved:\nПопробуем подать заявку заново??"
)

worker_warn_text = emojize(
    "Для <a href='tg://user?id={cid}'>{name}</a> <b>поставленно</b> предупреждение! ({warns}/3)."
)

worker_unwarn_text = emojize(
    "Для <a href='tg://user?id={cid}'>{name}</a> <b>снято</b> предупреждение ({warns}/3)."
)

statistic_text = emojize(
    ":monkey: Статистика проекта\n\n"
    "<i>Кол-во Воркеров</i>: <b>{workers_count}</b> (<i>{bot_users_count}</i>)\n"
    "<i>Кол-во Мамонтов Казик</i>: <b>{casino_count}</b>\n"
    "<i>Кол-во Мамонтов Эскорт</i>: <b>{escort_count}</b>\n"
    "<i>Кол-во Мамонтов Трейдинг</i>: <b>{trading_count}</b>\n\n"
    "<i>Общее кол-во профитов</i>: <b>{profits_count}</b>\n"
    "<i>Общая сумма профитов</i>: <b>{profits_amount} RUB</b>\n"
    "<i>Заработанно всего</i>: <b>{profits_cash} RUB</b>\n"
    "<i>Средний профит на воркера</i>: <b>{profits_middle} RUB</b>\n\n"
    ":anchor: Статистика за сегодня\n"
    "<i>Новых воркеров</i>: <b>{workers_count_today} (<i>{bot_users_count_today}</i>)</b>\n"
    "<i>Кол-во профитов</i>: <b>{profits_count_today}</b>\n"
    "<i>Сумма профитов</i>: <b>{profits_amount_today} RUB</b>\n"
    "<i>Средний профит сегодня</i>: <b>{profits_middle_today} RUB</b>\n"
    "<i>Заработанно сегодня</i>: <b>{profits_cash_today} RUB</b>\n"
)
