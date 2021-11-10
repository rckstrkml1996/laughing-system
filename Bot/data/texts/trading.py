from aiogram.utils.emoji import emojize

exact_out_text = emojize(
    "<b>Ваша заявка на вывод одобрена!</b>\n\n"
    ":money_with_wings: Сумма вывода: <b>{amount} RUB</b>"
)


trading_text = emojize(
    ":chart: <b>Трейд</b>\n\n"
    "Твой код: <code>{worker_id}</code>\n"
    "<a href='t.me/{trading_username}'>Скам бот</a>\n"
    "<a href='t.me/{trading_sup_username}'>Тех. поддержка</a>\n\n"
    "<a href='t.me/{trading_username}?start={worker_id}'>Реферальная ссылка</a>\n\n"
    "<a href='t.me/{reviews_link}'>Мануалы</a>\n\n"
    # "/info [<code>ID мамонта]</code> - инфо о мамонте\n"
    # "/del [<code>ID мамонта]</code> - удалить мамонта\n"
    # "/msg [<code>ID мамонта]</code>;[<code>Сообщение]</code> - сообщение от бота\n"
)
