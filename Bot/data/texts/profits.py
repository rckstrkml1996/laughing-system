from aiogram.utils.emoji import emojize


chat_profit_text = emojize(
    ":green_heart: <b><i>Новый</i></b> <a href='{profit_link}'>профит</a> ({service})\n"
    ":money_with_wings: Деньги: <b>{amount} RUB</b> ~ ({share} RUB)\n"
    ":man_technologist: Красавчик: {mention}"  # tag @{username} or mention
)

outs_profit_text = emojize(
    ":green_heart: <b><i>УСПЕШНАЯ</i></b> оплата ({service})\n\n"
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

unmatched_payment_text = emojize(
    "Qiwi - <b>id{qiwi_id}</b>\n"
    "Неизвестная транзакция.\n"
    "Сумма: <b>{amount} {currency}</b>\n"
)

# profit_complete_text = emojize(
#     "Успешно выплачено {share} RUB - <a href='{profit_link}'>профит</a> у "
#     "<a href='tg://user?id={cid}'>{name}</a>\n\n"
#     "Сервис: <b>{service}</b>\n"
#     "Сумма: <b>{amount}</b>"
# )

# profit_worker_text = emojize(
#     ":white_check_mark: У тебя новый профит! (<i>{service}</i>)\n\n"
#     ":money_with_wings: Мамонт закинул: <b>{amount} RUB</b>\n"
#     ":gem: Твоя доля: <b>{share} RUB</b>\n\n"
#     "ID Мамонта: /c{mid}\n\n"
#     "Cпасибо за ворк! :green_heart:"
# )

# profit_worker_hide = emojize("Скрылся :green_heart:")
