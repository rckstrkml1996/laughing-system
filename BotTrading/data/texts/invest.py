from aiogram.utils.emoji import emojize

agree_ecn = "<b><i>Ознакомьтесь с соглашением, чтобы открыть ECN Счёт!</i></b>"
ecn_agreed = emojize(
    ":white_check_mark: Вы ознакомились и согласились с <a href='{link}'>соглашением</a>!"
)

active_info = emojize(
    ":small_orange_diamond: {name} - <b>{price_usd:.2f} USD</b> (~ <i>{price_rub:.2f} RUB</i>)"
)

invest = emojize(
    "<b>Выберите актив</b> :point_down:\n\n"
    "{active_infos}\n\n"
    "<i>Данные о криптовалюте представлены - Coinbase, о валюте Morningstar</i>"
)

currency_info = emojize(
    "<b>{currency_name}</b>\n\n"
    "<a href='{photo_url}'>:small_orange_diamond:</a> Символ: <b>{symbol}</b>\n"
    ":money_with_wings: Стоимость: <b>{price_usd:.2f} USD</b> ~ (<i>{price_rub:.2f} RUB</i>)\n\n"
    "{description}"
)

bet_amount_insert = emojize(
    ":small_orange_diamond: <b>{currency_name}</b>\n"
    ":money_with_wings: Баланс: <b>{amount} RUB</b>\n\n"
    "<i>Введите сумму пула</i>"
)

non_digit_bet_amount = emojize(
    ":x: Сумма пула должна быть <b>числом</b>!\n\n<i>Введите сумму пула</i>"
)

too_big_bet_amount = emojize(
    ":x: Сумма пула слишком <b>большая</b>!\n"
    "Ваш баланс: <b>{amount} RUB</b>\n\n"
    "<i>Введите сумму пула</i>"
)

choice_fix_time = emojize(
    ":stopwatch: <b>Выберите</b>, через сколько времени должна произойти фиксация"
)

up_invest_type = emojize("Повышение :arrow_up_small:")
down_invest_type = emojize("Понижение :arrow_down_small:")

invest_going = emojize(
    "<b>{invest_type}</b>\n\n"  # понижение/повышение
    ":currency_exchange: Валюта: <b>{symbol}</b>\n"
    ":moneybag: Сумма пула: <b>{amount} RUB</b>\n\n"
    ":money_with_wings: Начальная цена: <b>{price_usd:.2f} USD</b> (~ <i>{price_rub:.2f} RUB</i>)\n"
    ":dollar: Цена сейчас: <b>{price_now_usd:.2f} USD</b> (~ <i>{price_now_rub:.2f} RUB</i>)\n\n"
    ":alarm_clock: Время: <b>{seconds}/{seconds_reached} <i>Секунд</i></b>"
)

invest_up_good = emojize(
    ":arrow_up_small: <b>За {seconds} секунд цена выросла!</b>\n\n"
    ":white_check_mark: Ваш пул удачный, <b>+{amount} RUB</b>\n"
    ":money_with_wings: Баланс: <b>{balance} RUB</b>"
)

invest_up_bad = emojize(
    ":arrow_up_small: <b>За {seconds} секунд цена упала!</b>\n\n"
    ":x: Ваш пул неудачный, <b>-{amount} RUB</b>\n"
    ":money_with_wings: Баланс: <b>{balance} RUB</b>"
)

invest_down_good = emojize(
    ":arrow_down_small: <b>За {seconds} секунд цена упала!</b>\n\n"
    ":white_check_mark: Ваша пул удачный, <b>+{amount} RUB</b>\n"
    ":money_with_wings: Баланс: <b>{balance} RUB</b>"
)

invest_down_bad = emojize(
    ":arrow_down_small: <b>За {seconds} секунд цена выросла!</b>\n\n"
    ":x: Ваша пул неудачный, <b>-{amount} RUB</b>\n"
    ":money_with_wings: Баланс: <b>{balance} RUB</b>"
)
