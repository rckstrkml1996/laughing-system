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
    "Информация по киви кошелькам.\n\n"
    "Общий баланс: <b>{all_balance} RUB</b>"
)

no_qiwis_text = emojize(
    "У вас нету привязанных кошельков!"
)

qiwi_error_text = emojize(
    "Какая то ошибка в киви, попробуй еще раз или позови кодера) :warning:"
)

add_qiwis_text = emojize(
    "Введите <b>Номер</b> и <b>Токен</b>, пример:\n"
    "<code>79008882211</code>\n"
    "<code>f420543a9430065db1264535ff4eb1ae</code>"
)

invalid_newqiwi_text = emojize(
    "Допущена ошибка при вводе! :warning:\n"
    "Введите <b>Номер</b> и <b>Токен</b>, пример:\n"
    "<code>79008882211</code>\n"
    "<code>f420543a9430065db1264535ff4eb1ae</code>"
)

qiwi_info_text = emojize(
    "Кошелек: <b>+{number}</b> :kiwi_fruit:\n"
    "Баланс: <b>{balance}</b>\n"
    "Последние транзакции :point_down:\n"
    "{last_actions}"
)

same_qiwi_text = emojize(
    "Похоже вы пытаетесь добавить такой же киви кошелек)"
)

qiwi_delete = emojize(
    ":wastebasket: Удаляю кошелек {account}\n"
    "Токен: {token}"
)

alert_text = emojize(
    "Отправка сообщения <b>всем</b> пользователя бота.\n"
    ":face_with_monocle: Выберите бота для оповещений."
)

make_alert_text = emojize(
    "Отравка всем пользователям <b>{bot_type}</b>\n"
    ":imp: Введите текст:"
)

edit_alert_text = emojize(
    "Отравка всем пользователям <b>{bot_type}</b>\n"
    ":imp: Введите <b>новый</b> текст:"
)

alert_accept_text = emojize(
    ":thinking_face: Вы уверенны что хотите отправить это?\n\n{text}"
)

alert_reject_text = emojize(
    ":wastebasket: Текст <b>не будет</b> отправлен!"
)

alert_start_text = emojize(
    "Начинаю рассылку всем пользователям.\n"
    "Кол-во пользователей: <b>{len_users}</b>\n\n"
    "Сообщений отправленно: <b>{msg_count}</b>\n"
    "Заблокировали бота: <b>{blocked_count}</b>\n"
    "Не найдено: <b>{not_found_count}</b>"
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
