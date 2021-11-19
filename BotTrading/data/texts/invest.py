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

up_invest_type = emojize("Повышение :arrow_up_small:")
down_invest_type = emojize("Понижение :arrow_down_small:")

invest_going = emojize(
    "<b>{invest_type}</b>\n\n"  # понижение/повышение
    ":currency_exchange: Валюта: {symbol}\n"
    ":moneybag: Сумма ставки: <b>{amount} RUB</b>\n"
    ":money_with_wings: Цена в начале ставки: <b>{price_usd} USD</b> (~ <i>{price_rub} RUB</i>)\n\n"
    ":dollar: Цена сейчас: <b>{price_now} USD</b>\n\n"
    ":alarm_clock: Время: <b>{seconds}:{seconds_reached} <i>Секунд</i></b>"
)

invest_up_good = emojize(
    ":arrow_up_small: <b>За {seconds} секунд цена выросла!</b>\n\n"
    ":white_check_mark: Ваша ставка удачная, <b>+{amount} RUB</b>\n"
    ":money_with_wings: Баланс: <b>{balance} RUB</b>"
)

invest_up_bad = emojize(
    ":arrow_up_small: <b>За {seconds} секунд цена выросла!</b>\n\n"
    ":x: Ваша ставка неудачная, <b>-{amount} RUB</b>\n"
    ":money_with_wings: Баланс: <b>{balance} RUB</b>"
)

invest_down_good = emojize(
    ":arrow_down_small: <b>За {seconds} секунд цена упала!</b>\n\n"
    ":white_check_mark: Ваша ставка удачная, <b>+{amount} RUB</b>\n"
    ":money_with_wings: Баланс: <b>{balance} RUB</b>"
)

invest_down_bad = emojize(
    ":arrow_down_small: <b>За {seconds} секунд цена упала!</b>\n\n"
    ":x: Ваша ставка неудачная, <b>-{amount} RUB</b>\n"
    ":money_with_wings: Баланс: <b>{balance} RUB</b>"
)
