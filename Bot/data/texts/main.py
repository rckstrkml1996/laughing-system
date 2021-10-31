import os

from aiogram.utils.emoji import emojize

from loader import config

zap_text = emojize(":zap:")

worker_defenition = "<a href='tg://user?id={chat_id}'>{name}</a>"


new_username_text = emojize(
    ":sneezing_face: <a href='tg://user?id={chat_id}'>{name}</a> сменил свой ник с <b>{old_username}</b> на <b>{new_username}</b>"
)

outs_link = config.outs_link
reviews_link = config.reviews_link

new_chat_member_text = emojize(
    ":green_heart: Привет, <a href='tg://user?id={chat_id}'>{name}</a>\n"
    ":gem: <a href='t.me/{bot_username}'>Бот для всего</a>\n"
    f":money_with_wings: <a href='t.me/{outs_link}'>Выплаты</a>\n"
    ":fire: Процент выплат в смотри <b>закрепе</b>\n"
    f":credit_card: Пополнения от <b>{config.min_deposit} RUB</b>"
)

# multy use
services_status = (
    "{casino_status}\n" "{escort_status}\n" "{trading_status}\n" "{team_status}"
)


# inline use
about_worker_text = "{status}\n{profits} на сумму {profits_sum} р"

startup_text = emojize("Бот <b>запущен</b>! :sparkle:")
updated_startup_text = emojize("Бот <b>запущен и обновился</b>! :chart:")


pin_help_text = emojize(
    ":woman_tipping_hand: Сокращения для динамического закрепа:\n\n"
    "<code>{services_status}</code> - Статусы работы проекта\n"
    "<code>{topd_worker}</code> - Лучший воркер за день\n"
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
