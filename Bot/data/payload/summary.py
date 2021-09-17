from aiogram.utils.emoji import emojize

from config import config

"""
    Summary

"""

summary_text = emojize(
    ":man_shrugging: <b>Неизвестная команда.</b>\n"
    ":snake: <b>Хотите подать заявку?</b>"
)

new_summary_text = emojize(
    f"Привет, это бот <b>{config('team_name').upper()}</b> :revolving_hearts:\n"
    "Чтобы начать работу у нас, подай заявку :point_down:"
)


def rules_text(agreed=False):
    text = (
        ":page_with_curl: <b>Правила нашего проекта:</b>\n\n"
        "• <code>Запрещено попрошайничество</code>\n\n"
        "• <code>Запрещен: спам/флуд/шок/порно контент</code>\n\n"
        "• <code>Запрещается продажа каких либо услуг/товаров без соглашения администрации, за сделки проведённые без нашего ведома ответственности НЕ НЕСЁМ</code>\n\n"
        "• <code>Запрещено принимать оплату на свои реквизиты</code>\n\n"
        "• <code>Разрешено - рофлить над всеми, не зависимо от статуса участника проекта (в пределах нормы)</code>\n\n"
        "• <code>По усмотрению администрации проекта, лок/скам дропов ОПЛАЧИВАЕТСЯ в размере 25%-50% от успешной оплаты</code>"
    )

    if agreed:
        text += ":white_check_mark: <b>Вы ознакомились и согласились с правилами проекта</b>"
    else:
        text += ":grey_question: Вы подтверждаете, что ознакомились и согласны с условиями и правилами нашего проекта?"

    return emojize(text)


summary_where_text = emojize(
    ":seedling: <b>Откуда Вы узнали о нас?</b>\n\n" "Отправьте ссылку на источник."
)

summary_exp_text = emojize(
    ":dragon: <b>Есть ли у вас опыт работы в данной сфере?</b>\nПриложите доказательства:\n\n"
    "• <code>Скрины выплат из команд где вы работали</code>\n"
    "• <code>Скриншот 'Мой профиль' (если имеется в боте)</code>\n"
    "• <code>Общая сумма оплат</code>\n\n"
    "Можно отправить ссылку из [@imgurbot_bot] или просто прислать фото."
)

summary_final = emojize(
    ":love_letter: <b>Ваша заявка готова к отправке на проверку!</b>\n\n"
    ":one: Откуда Вы узнали о нас: <b>{where}</b>\n"
    ":two: Ваш опыт работы: <b>{experience}</b>"
)

summary_sended_text = emojize(
    ":file_folder: <b>Ваша заявка отправлена на проверку</b>\n\n"
    "Вам придет уведомление когда заявку рассмотрят!\n\n"
    ":one: <b>Откуда Вы узнали о нас:</b> {where}\n"
    ":two: <b>Ваш опыт работы:</b> {experience}"
)

summary_reviewing_text = emojize(
    ":warning: <b>Ошибка!</b>\n" ":information_source: Ваша заявка уже рассматривается"
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
    ":shrimp: <b>Вы пришли нахуй!</b>\n\n" "<code>Иди отсоси себе)</code>"
)
