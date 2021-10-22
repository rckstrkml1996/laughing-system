import os

from aiogram.utils.emoji import emojize

from config import config


zap_text = emojize(":zap:")

worker_defenition = "<a href='tg://user?id={chat_id}'>{name}</a>"


new_username_text = emojize(
    ":sneezing_face: <a href='tg://user?id={chat_id}'>{name}</a> сменил свой ник с <b>{old_username}</b> на <b>{new_username}</b>"
)

outs_link = config("outs_link")
reviews_link = config("reviews_link")

new_chat_member_text = emojize(
    ":green_heart: Привет, <a href='tg://user?id={chat_id}'>{name}</a>\n"
    ":gem: <a href='t.me/{bot_username}'>Бот для всего</a>\n"
    f":money_with_wings: <a href='t.me/{outs_link}'>Выплаты</a>\n"
    ":fire: Процент выплат в смотри <b>закрепе</b>\n"
    f":credit_card: Пополнения от <b>{config('min_deposit', int)} RUB</b>"
)

# multy use
services_status = (
    "{casino_status}\n" "{escort_status}\n" "{trading_status}\n" "{team_status}"
)


# inline use
about_worker_text = "{status}\n{profits} на сумму {profits_sum} р"

startup_text = emojize("Бот <b>запущен</b>! :sparkle:")
updated_startup_text = emojize("Бот <b>запущен и обновился</b>! :chart:")


# dynamic pin

standart_pin = emojize("Стандартный закреп, {time} :sparkle:")

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

top_none_text = emojize(":coffin: <b>Топ пустой.</b>")

top_text = emojize(
    ":woman_raising_hand: Топ воркеров за {period}:\n\n"
    "{profits}\n\n"
    ":money_with_wings: Общий профит - <b>{all_profits}</b> RUB"
)


profit_text = emojize(
    ":white_check_mark: <b><i>УСПЕШНАЯ</i></b> оплата ({service})\n\n"
    ":money_with_wings: Мамонт депнул: <b>{amount} RUB</b>\n"
    ":gem: Доля воркера: <b>{share} RUB</b>\n\n"
    ":man_technologist: Воркер: {link}"
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

profit_worker_text = emojize(
    ":white_check_mark: Бро у тебя новый профит! (<i>{service}</i>)\n"
    ":money_with_wings: Мамонт депнул: <b>{amount}</b> RUB\n"
    ":gem: Твоя доля ~ <b>{share} RUB</b>\n\n"
    "ID Мамонта: /c{mid}\n\n"
    "Cпасибо за ворк :green_heart:"
)
