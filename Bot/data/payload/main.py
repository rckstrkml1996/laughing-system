import os

from aiogram.utils.emoji import emojize

from config import Rates, config


# multy use
services_status = (
    "{casino_status}\n" "{escort_status}\n" "{trading_status}\n" "{team_status}"
)


# inline use
about_worker_text = "{status}\n{profits} на сумму {profits_sum} р"

startup_text = emojize("<b>Бот запущен!</b> :sparkle:")


# dynamic pin

standart_pin = emojize("СТАНДАРТНЫЙ КОНФИГ {time}")

pin_path = config("pin_path")

if not os.path.exists(pin_path):
    fl = open(pin_path, "w", encoding="utf-8")
    fl.write(standart_pin)
    fl.close()


def pin_text():
    fl = open(pin_path, "r", encoding="utf-8")
    pin = fl.read()
    fl.close()
    return pin


pin_help_text = emojize(
    ":woman_tipping_hand: Сокращения для динамического закрепа:\n\n"
    "<code>{dyna_moon}</code> - Луна которая зависит от статуса проекта\n"
    "<code>{services_status}</code> - Статусы работы проекта\n"
    "<code>{topd_worker}</code> - Лучший воркер за день\n"
    "<code>{btc_usd_price}</code> - Цена биткоина в долларах\n"
    "<code>{btc_rub_price}</code> - Цена биткоина в рублях\n"
    "<code>{in_casino}</code> - Кол-во мамонтов в казино\n"
    "<code>{in_trading}</code> - Кол-во мамонтов в трейдинге\n"
    "<code>{in_escort}</code> - Кол-во мамонтов в эскорте\n"
    "<code>{time}</code> - Время Час:Минута, Секунда"
)

top_text = emojize(
    ":woman_raising_hand: Топ воркеров за {period}:\n\n"
    "{profits}\n\n"
    ":money_with_wings: Общий профит - <b>{all_profits}</b> RUB"
)


profits_text = emojize(":lizard: Какую статистику отобразить?")

week_profitinv_text = emojize("Список Ваших профитов за неделю пуст.")

week_profit_text = emojize(
    ":chart: Статистика за неделю.\n\n"
    "<b>Средний чек:</b> {middle_profits:.0f} RUB\n"
    "<b>Кол-во залетов:</b> {profits_len}"
)

profit_text = emojize(
    ":white_check_mark: <b>УСПЕШНАЯ</b> оплата ({service})\n"
    ":money_with_wings: Мамонт депнул: <b>{amount} ₽</b>\n\n"
    ":gem: <b>Доля</b> воркера ~ <b>{share} ₽</b>\n"
    ":computer: Воркер: <a href='tg://user?id={cid}'>{name}</a>"
)

admins_profit_text = emojize(
    ":call_me_hand: Новый <a href='{profit_link}'>профит</a> у <a href='tg://user?id={cid}'>{name}</a>\n\n"
    "Сервис: <b>{service}</b>\n"
    "Сумма: <b>{amount} RUB</b>\n"
    "Будет выплачено: <b>{share} RUB</b> (<i>{moll}%</i>)\n\n"
    "Дата создания пополнения: {create_date}\n"
    "Дата оплаты пополнения: {pay_date}"
)

profit_complete_text = emojize(
    "Успешно выплачено {share} RUB - <a href='{profit_link}'>профит</a> у <a href='tg://user?id={cid}'>{name}</a>\n\n"
    "Сервис: <b>{service}</b>\n"
    "Сумма: <b>{amount}</b>"
)
