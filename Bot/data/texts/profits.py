from aiogram.utils.emoji import emojize


chat_profit_text = emojize(
    ":green_heart: <b><i>Новый</i></b> <a href='{profit_link}'>профит</a> ({service})\n"
    ":money_with_wings: Деньги: <b>{amount} RUB</b> ~ ({share} RUB)\n"
    ":man_technologist: Красавчик: {mention}"  # tag @{username} or mention
)

outs_profit_text = emojize(
    ":green_heart: <b><i>Успешная</i></b> оплата ({service})\n\n"
    ":money_with_wings: Мамонт депнул: <b>{amount} RUB</b>\n"
    ":gem: Доля воркера: <b>{share} RUB</b>\n\n"
    ":man_technologist: Воркер: {mention}"
)

admins_profit_text = emojize(
    ":call_me_hand: Новый <a href='{profit_link}'>профит</a> у {mention}\n\n"
    "Сервис: <b>{service}</b>\n"
    "Сумма: <b>{amount} RUB</b>\n"
    "Будет выплачено: <b>{share} RUB</b> (<i>{moll}%</i>)\n\n"
    "Дата создания пополнения: {create_date}\n"
    "Дата оплаты пополнения: {pay_date}"
)

admins_profit_complete_text = emojize(
    ":call_me_hand: Выплачен <a href='{profit_link}'>профит</a> у {mention}\n\n"
    "Сервис: <b>{service}</b>\n"
    "Сумма: <b>{amount} RUB</b>\n"
    "Будет выплачено: <b>{share} RUB</b> (<i>{moll}%</i>)\n\n"
)

unmatched_payment_text = emojize(
    "Неизвестная транзакция.\n" "Сумма: <b>{amount} {currency}</b>\n"
)

make_profit_text = emojize(
    "Заполни данные:\n"
    "<code>1444022512</code> - <i>Telegram ID Воркера</i>\n"
    "<code>1000</code> - <i>Сумма залета</i>\n"
    "<code>70</code> - <i>Процент залета</i>\n"
    "<code>Казино</code> - <i>Название сервиса</i>\n"
)

profit_check_text = emojize(
    ":green_heart: Твоя выплата, <b>спасибо за ворк</b>!\n\n"
    "Сумма залета: <b>{amount} RUB</b>\n"
    "Сумма чека: <b>{share} RUB</b>\n\n<b><i>{check}</i></b>"
)


worker_profit_text = emojize(
    ":green_heart: У тебя новый <a href='{profit_link}'>профит</a>! (<i>{service}</i>)\n\n"
    ":money_with_wings: Мамонт пополнил: <b>{amount} RUB</b>\n"
    ":gem: Ты получишь: <b>{share} RUB</b>\n\n"
    "ID Мамонта: /c{mid}\n\n"
    "Cпасибо за ворк! :tada:"
)

worker_manual_profit_text = emojize(
    ":green_heart: Тебе создали <a href='{profit_link}'>профит</a>! (<i>{service}</i>)\n\n"
    ":money_with_wings: Сумма: <b>{amount} RUB</b>\n"
    ":gem: Доля: <b>{share} RUB</b>\n\n"
    "Спасибо за работу!! :tada:"
)
