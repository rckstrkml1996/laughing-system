import os

from aiogram.utils.emoji import emojize

from config import Rates, config

# multy use
services_status = "{casino_status}\n" \
    "{escort_status}\n" \
    "{antikino_status}\n" \
    "{team_status}"


# inline use
about_worker_text = "{status}\n{profits} на сумму {profits_sum} р"

startup_text = emojize(
    "<b>Бот запущен!</b> :sparkle:"
)

"""
    Summary

"""

summary_text = emojize(
    ":man_shrugging: <b>Неизвестная комманда.</b>\n"
    ":snake: <b>Хотите подать заявку?</b>"
)

new_summary_text = emojize(
    "Привет, это бот <b>DUREX TEAM</b> :revolving_hearts:\n"
    "Чтобы начать работу у нас, подай заявку :point_down:"
)


def rules_text(agreed=False):
    text = ":page_with_curl: <b>Правила нашего проекта:</b>\n\n" \
        "• <code>Запрещено попрошайничество</code>\n\n" \
        "• <code>Запрещен: спам/флуд/шок/порно контент</code>\n\n" \
        "• <code>Запрещается продажа каких либо услуг/товаров без соглашения администрации, за сделки проведённые без нашего ведома ответственности НЕ НЕСЁМ</code>\n\n" \
        "• <code>Запрещено принимать оплату на свои реквизиты</code>\n\n"  \
        "• <code>Разрешено - рофлить над всеми, не зависимо от статуса участника проекта (в пределах нормы)</code>\n\n" \
        "• <code>По усмотрению администрации проекта, лок/скам дропов ОПЛАЧИВАЕТСЯ в размере 25%-50% от успешной оплаты</code>"

    if agreed:
        text += ":white_check_mark: <b>Вы ознакомились и согласились с правилами проекта</b>"
    else:
        text += ":grey_question: Вы подтверждаете, что ознакомились и согласны с условиями и правилами нашего проекта?"

    return emojize(text)


summary_where_text = emojize(
    ":seedling: <b>Откуда Вы узнали о нас?</b>\n\n"
    "Отправьте ссылку на источник."
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
    ":warning: <b>Ошибка!</b>\n"
    ":information_source: Ваша заявка уже рассматривается"
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
    ":woman_tipping_hand: <b>Твой профиль</b>\n\n"
    ":rocket: Telegram ID: <b>{chat_id}</b>\n"
    "Реф баланс: <b>{ref_balance} RUB</b>\n\n"
    ":money_with_wings: У тебя {len_profits} профитов на сумму <b>{all_balance}₽</b>\n"
    "Средний профит ~ <b>{middle_profits}₽</b>\n\n"
    ":gem: Приглашено: <b>0 воркеров</b>\n\n"
    "Статус: <b>{status}</b>\n\n"
    ":warning: Предупреждений: <b>[{warns}/3]</b>\n"
    "В команде: <b>{in_team}</b>\n\n"
    "{team_status}"
)

about_project_text = emojize(
    ":woman_tipping_hand: <b>Информация о проекте Hide Team</b>\n\n"
    ":fire: Мы открылись: {team_start}\n"
    ":fallen_leaf: Количество профитов: {team_profits}\n"
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


# for chat commands

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

# dynamic pin

standart_pin = emojize(
    "СТАНДАРТНЫЙ КОНФИГ"
)

pin_path = config("pin_path")

if not os.path.exists(pin_path):
    fl = open(pin_path, "w")
    fl.write(standart_pin)
    fl.close()


def pin_text():
    fl = open(pin_path, "r")
    pin = fl.read()
    fl.close()
    return pin


top_text = emojize(
    ":woman_raising_hand: Топ воркеров за {period}:\n\n"
    "{profits}\n\n"
    ":money_with_wings: Общий профит - <b>{all_profits}</b> RUB"
)

# admins commands

adm_work_command = emojize(
    "<b>Состояние</b> сервисов:\n"
    "{services_status}"
)

setwork_text = emojize(":white_check_mark: <b>Поставлен</b> ворк")
setdontwork_text = emojize(":x: <b>Поставлен</b> неворк")
