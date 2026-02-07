from aiogram.utils.emoji import emojize


worker_menu_text = emojize(
    ":green_apple: <b>Твой профиль</b> [<code>{chat_id}</code>]\n\n"
    ":closed_lock_with_key: Код для сервисов: <code>{uniq_key}</code>\n"
    ":cold_face: <i>Реф баланс:</i> {ref_balance} RUB\n\n"
    ":money_with_wings: У тебя {profits} на сумму <b>{all_balance} RUB</b>\n"
    "Средний профит <b>{middle_profits} RUB</b>\n\n"
    ":gem: Приглашено: <b>{invited_count} воркеров</b>\n"
    ":man_technologist: Статус: <b>{status}</b>\n"
    ":warning: Предупреждений: [<b>{warns}/3</b>]\n"
    ":hourglass_flowing_sand: <i>В команде:</i> {in_team}\n\n"
    "{team_status}"
)

about_project_text = emojize(
    ":woman_tipping_hand: <b>Информация о проекте {team_name}</b>\n\n"
    ":fire: Мы открылись: {team_start}\n"
    ":money_with_wings: Количество профитов: <b>{team_profits}</b>\n"
    ":moneybag: Общая сумма профитов: <b>{profits_sum} RUB</b>\n\n"
    "<b>Выплаты</b> проекта:\n"
    "Залет - <b>80%</b>\n"
    "Иксы - <b>70%</b>\n\n"
    "<b>Состояние</b> сервисов: \n"
    "{services_status}"
)

referral_system_text = emojize(
    ":scream: Реферальная система\n\n"
    "<i>Приглашайте новых пользователей!</i>\n"
    "Чтобы пользователь стал вашим рефералом:\n\n"
    "1. При заполнении анкеты, он должен указать в пункте «<b>Кто вас пригласил?</b>» "
    "ваш Telegram ID - <b>{user_id}</b>.\n"
    "2. Он должен перейти по вашей ссылке - {start_link}\n\n"
    "В случае принятия данного пользователя в команду, он становится <b>вашим</b> рефералом."
)
