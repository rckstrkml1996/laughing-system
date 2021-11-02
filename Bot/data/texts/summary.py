from aiogram.utils.emoji import emojize


summary_text = emojize(
    "<b>Неизвестная команда.</b> :man_shrugging:\n"
    "Хотите <b>подать заявку</b>? :snake:"
)

new_summary_text = emojize(
    "Привет, это бот <b>{team_name}</b> :snake:\n"
    "Чтобы начать работу у нас, подай заявку :cold_face:"
)


def rules_text(agreed=False):
    text = (
        ":page_with_curl: <b>Правила нашего проекта:</b>\n\n"
        "• <code>Запрещено попрошайничество</code>\n"
        "• <code>Запрещен: <b>спам</b>/флуд/шок/порно контент</code>\n"
        "• <code>Запрещается продажа каких либо услуг/товаров без соглашения администрации, за сделки проведённые без нашего ведома ответственности НЕ НЕСЁМ</code>\n"
        "• <code>Запрещено принимать оплату на свои реквизиты</code>\n"
        "• <code>Разрешено - рофлить над всеми, не зависимо от статуса участника проекта (в пределах нормы)</code>\n"
        "• <code>Локи выплачиваются по усмотрению ТСа.</code>\n"
        "• <code>Мануалы по ворку не продавать!</code>\n\n"
        "• <code>Кодира не бить по ебалу</code>\n\n"
    )

    if agreed:
        text += "<b>Вы ознакомились и согласились с правилами проекта</b> :white_check_mark:"
    else:
        text += ":grey_question: <b>Вы подтверждаете, что ознакомились и согласны с условиями и правилами нашего проекта?</b>"

    return emojize(text)


summary_where_text = emojize(
    "<b>Откуда Вы узнали о нас?</b> :seedling:\n\n"
    "Пожалуйста отправьте <b>линк</b> на источник."
)

summary_exp_text = emojize(
    "<b>У вас есть опыт работы в такой сфере?</b> :dragon:\n"
    "Приложите доказательства:\n\n"
    "• <code>Скрины выплат из команд где вы работали</code>\n"
    "• <code>Скриншот 'Мой профиль' (если имеется в боте)</code>\n"
    "• <code>Общая сумма оплат</code>\n\n"
    "Можно отправить ссылку из [@imgurbot_bot]."
)

summary_final = emojize(
    ":love_letter: <b>Ваша заявка готова к отправке на проверку!</b>\n\n"
    ":one: Откуда Вы узнали о нас: <b>{where}</b>\n"
    ":two: Ваш опыт работы: <b>{experience}</b>"
)

summary_sended_text = emojize(
    ":snake: <b>Ваша заявка на проверке.</b>\n\n"
    "Бот скажет когда тебя примут!\n\n"
    ":one: <b>Откуда Вы узнали о нас:</b> {where}\n"
    ":two: <b>Ваш опыт работы:</b> {experience}"
)

summary_reviewing_text = emojize(
    ":warning: <b>Ошибка!</b>\n" ":information_source: Ваша заявка уже рассматривается)"
)


def summary_check_text(status="Ожидает проверки"):
    if status == "Ожидает проверки":
        text = emojize(":envelope: <b>Поступила заявка на вступление</b>\n\n")
    else:
        text = ""

    text += emojize(
        "<b>{name}</b> {username}[<code>{chat_id}</code>]\n\n"
        ":one: Откуда Вы узнали о нас: <b>{where}</b>\n"
        ":two: Ваш опыт работы: <b>{experience}</b>\n\n"
        "<b>Статус:</b> "
    )

    text += status

    return text


summary_rejected_text = emojize(
    ":warning: <b>Администрация проекта отклонила Вашу заявку!</b>\n"
    ":link: <b>Попробуйте подать заявку заново.</b>"
)

summary_accepted_text = emojize(
    ":tada: <b>Ваша заявка на вступление одобрена</b>\n\n"
    "Вступайте в чат и начинайте работать!\n"
    "<b>Удачных профитов!</b>"
)

summary_blocked_text = emojize(
    ":no_entry_sign: <b>Администрация проекта заблокировала Вас!</b>\n\n"
    ":hatched_chick: <b>Ты идешь НАХУЙ!</b>"
)

summary_blockfin_text = emojize(
    ":shrimp: <b>Вы пришли нахуй!</b>\n"
    "Кодер вас не любит. :angry:\n\n"
    "<code>Иди отсоси себе)</code>"
)
