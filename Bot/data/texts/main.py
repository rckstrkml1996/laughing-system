from aiogram.utils.emoji import emojize


startup_text = emojize("<b>Бот <i>запущен</i>!</b> :sparkle:")
updated_startup_text = emojize("<b>Бот <i>запущен и обновился</i>!</b> :chart:")


zap_text = emojize(":zap:")


new_username_text = emojize(
    "<a href='tg://user?id={chat_id}'>{name}</a> сменил свой ник с <b>@{old_username}</b> на <b>@{new_username}</b> :poop:"
)

new_chat_member_text = emojize(
    ":green_heart: Привет, <a href='tg://user?id={chat_id}'>{name}</a>\n"
    ":gem: <a href='t.me/{bot_username}'>Бот для всего</a>\n"
    ":money_with_wings: <a href='t.me/{outs_link}'>Выплаты</a>\n"
    ":fire: Процент выплат в смотри <b>закрепе</b>\n"
    ":credit_card: Пополнения от <b>{min_deposit} RUB</b>"
)

# multy use
services_status = "{casino_status}\n{escort_status}\n{trading_status}\n{team_status}"


# inline use
about_worker_text = "{status}\n{profits} на сумму {profits_sum} RUB"


top_none_text = emojize(":coffin: <b>Топ пустой.</b>")

top_text = emojize(
    ":man_technologist: Топ воркеров за {period}:\n\n"
    "{profits}\n\n"
    ":money_with_wings: Общий профит - <b>{all_profits}</b> RUB"
)


worker_choice_one_plz = emojize(
    ":weary: Выбери один из <b>{status_len}</b> предложенных статусов!"
)

set_new_worker_status = emojize(
    ":see_no_evil: Установил новый статус <b>{status_name}</b> для {mention}"
)  # {worker_defenition.format(chat_id=diff_worker.cid, name=diff_worker.name)}
