from aiogram.utils.emoji import emojize

active_info = emojize(
    ":small_orange_diamond: {name} - <b>{price_usd} USD</b> (~ <i>{price_rub} RUB</i>)"
)

invest = emojize(
    "<b>Выберите актив</b> :point_down:\n\n"
    "{active_infos}\n\n"
    "<i>Данные о криптовалюте представлены - Coinbase, о валюте Morningstar</i>"
)

currency_info = emojize(
    "<b>{currency_name}</b>\n\n"
    "<a href='{photo_url}'>:small_orange_diamond:</a> Символ: <b>{symbol}</b>\n"
    ":money_with_wings: Стоимость: <b>{price_usd} USD</b> ~ (<i>{price_rub} RUB</i>)\n\n"
    "{description}"
)

bet_amount_insert = emojize(
    ":small_orange_diamond: <b>{currency_name}</b>\n"
    ":money_with_wings: Баланс: <b>{amount} RUB</b>\n\n"
    "<i>Введите сумму ставки</i>"
)

non_digit_bet_amount = emojize(
    ":x: Сумма ставки должна быть <b>числом</b>!\n\n<i>Введите сумму ставки</i>"
)

too_big_bet_amount = emojize(
    ":x: Сумма ставки слишком <b>большая</b>!\n"
    "Ваш баланс: <b>{amount} RUB</b>\n\n"
    "<i>Введите сумму ставки</i>"
)

choice_fix_time = emojize(
    ":stopwatch: <b>Выберите</b>, через сколько времени должна произойти фиксация"
)

up_invest_type = emojize("Повышение :arrow_up_small:")
down_invest_type = emojize("Понижение :arrow_down_small:")

invest_going = emojize(
    "<b>{invest_type}</b>\n\n"  # понижение/повышение
    ":currency_exchange: Валюта: <b>{symbol}</b>\n"
    ":moneybag: Сумма ставки: <b>{amount} RUB</b>\n"
    ":money_with_wings: Цена в начале ставки: <b>{price_usd} USD</b> (~ <i>{price_rub} RUB</i>)\n\n"
    ":dollar: Цена сейчас: <b>{price_now_usd:.2f} USD</b> (~ <i>{price_now_rub:.2f} RUB</i>)\n\n"
    ":alarm_clock: Время: <b>{seconds}/{seconds_reached} <i>Секунд</i></b>"
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
