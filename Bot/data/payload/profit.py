from aiogram.utils.emoji import emojize


profit_text = emojize(
    ":white_check_mark: <b><i>УСПЕШНАЯ</i></b> оплата ({service})\n\n"
    ":money_with_wings: Мамонт депнул: <b>{amount} RUB</b>\n"
    ":gem: Доля воркера: <b>{share} RUB</b>\n\n"
    ":man_technologist: Воркер: {link}"
)

admins_profit_text = emojize(
    ":call_me_hand: Новый <a href='{profit_link}'>профит</a> у "
    "<a href='tg://user?id={cid}'>{name}</a>\n\n"
    "Сервис: <b>{service}</b>\n"
    "Сумма: <b>{amount} RUB</b>\n"
    "Будет выплачено: <b>{share} RUB</b> (<i>{moll}%</i>)\n\n"
    "Дата создания пополнения: {create_date}\n"
    "Дата оплаты пополнения: {pay_date}"
)

profit_complete_text = emojize(
    "Успешно выплачено {share} RUB - <a href='{profit_link}'>профит</a> у "
    "<a href='tg://user?id={cid}'>{name}</a>\n\n"
    "Сервис: <b>{service}</b>\n"
    "Сумма: <b>{amount}</b>"
)

profit_worker_text = emojize(
    ":white_check_mark: У тебя новый профит! (<i>{service}</i>)\n\n"
    ":money_with_wings: Мамонт закинул: <b>{amount} RUB</b>\n"
    ":gem: Твоя доля: <b>{share} RUB</b>\n\n"
    "ID Мамонта: /c{mid}\n\n"
    "Cпасибо за ворк! :green_heart:"
)

profit_worker_hide = emojize("Скрылся :green_heart:")
