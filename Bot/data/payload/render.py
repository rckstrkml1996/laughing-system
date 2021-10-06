from aiogram.utils.emoji import emojize

render_main_text = "Что будем отрисовывать?"

render_qiwi_balance_text = emojize(
    "<b>Введите необходимые данные:</b>\n\n"
    ":one: Сумма перевода\n"
    ":two: Время скриншота\n\n"
    "<b>Пример:</b>\n"
    "<code>5024,59\n8:10</code>"
)

render_qiwi_trans_text = emojize(
    "<b>Введите необходимые данные:</b>\n\n"
    ":one: Номер получателя\n"
    ":two: Сумма перевода\n"
    ":three: Дата перевода\n\n"
    "<b>Пример:</b>\n"
    "<code>+78005553535\n500\n18.06.2021 в 6:56</code>"
)

render_sber_trans_text = emojize(
    "<b>Введите необходимые данные:</b>\n\n"
    ":one: Сумма перевода\n"
    ":two: ФИО Получателя\n"
    ":three: Время скриншота\n\n"
    "<b>Пример:</b>\n"
    "<code>10000\nИван Иванович\n6:36</code>"
)
