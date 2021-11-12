from aiogram.utils.emoji import emojize

active_info = "{name} - <b>{price_usd} USD</b> ~ <b>{price_rub} RUB</b>"

invest = emojize("Выберите актив\n\n{active_infos}")

currency_info = emojize(
    "<b>{currency_name}</b>\n\n"
    ":small_orange_diamond: Символ: <b>{symbol}</b>\n"
    ":money_with_wings: Стоимость: <b>{price_usd} USD</b> ~ (<i>{price_rub} RUB</i>)\n\n"
    "{description}"
)

bet_amount_insert = emojize(
    ":small_orange_diamond: {currency_name}\n"
    ":money_with_wings: Баланс: {amount} RUB\n\n"
    "Введите сумму ставки"
)

non_digit_bet_amount = emojize(
    ":x: Сумма ставки должна быть <b>числом</b>!\n\n" "Введите сумму ставки"
)

too_big_bet_amount = emojize(
    ":x: Сумма ставки слишком <b>большая</b>!\n"
    "Ваш баланс: <b>{amount} RUB</b>\n\n"
    "Введите сумму ставки"
)

choice_fix_time = emojize(
    ":stopwatch: <b>Выберите</b>, через сколько времени должна произойти фиксация"
)
