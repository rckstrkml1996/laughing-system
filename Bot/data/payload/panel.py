from aiogram.utils.emoji import emojize

from config import config

worker_menu_text = emojize(
    ":woman_tipping_hand: <b>Твой профиль</b> [<code>{chat_id}</code>]\n\n"
    "Реф баланс: <b>{ref_balance} RUB</b>\n\n"
    ":money_with_wings: У тебя {profits} на сумму <b>{all_balance}₽</b>\n"
    "Средний профит ~ <b>{middle_profits}₽</b>\n\n"
    ":gem: Приглашено: <b>0 воркеров</b>\n\n"
    "Статус: <b>{status}</b>\n\n"
    ":warning: Предупреждений: <b>[{warns}/3]</b>\n"
    "В команде: <b>{in_team}</b>\n\n"
    "{team_status}"
)

about_project_text = emojize(
    f":woman_tipping_hand: <b>Информация о проекте {config('team_name')}</b>\n\n"
    f":fire: Мы открылись: {config('team_start')}\n"
    "&#127468;&#127463; Количество профитов: {team_profits}\n"
    ":moneybag: Общая сумма профитов: {profits_sum} ₽\n"
    "<b>Выплаты</b> проекта:\n"
    "— Оплата - <b>80%</b>\n"
    "— Возврат - <b>70%</b>\n\n"
    "<b>Состояние</b> сервисов: \n"
    "{services_status}"
)

referral_system_text = emojize(
    ":woman_tipping_hand: <b>Реферальная</b> система\n\n"
    "Приглашайте новых пользователей!\n\n"
    "Чтобы пользователь стал вашим рефералом, при заполнении анкеты,\
    он должен указать в пункте <b>«Кто вас пригласил?»</b> ваш Telegram ID - <b>{user_id}</b> \n\n"
    "В случае принятия данного пользователя в команду, он становится вашим рефералом."
)
