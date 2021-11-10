from aiogram.utils.emoji import emojize


main_out_request = emojize(
    ":chart: <b>Новый запрос на вывод средств!</b> (Трейдинг)\n\n"
    ":elephant: Мамонт: {mention} [/t{user_id}]\n"
    ":money_with_wings: Сумма: <b>{amount} RUB</b>"
)

mention_text = "<a href='tg://user?id={user_id}'>{text}</a>"

main_new_user = emojize(":chart: <b>Новый мамонт!</b> (Трейдинг) {mention} /t{user_id}")

main_add_request = emojize(
    ":chart: <b>Новая заявка на пополнение!</b> (Трейдинг)\n\n"
    ":elephant: Мамонт: {mention} [/t{user_id}]\n"
    ":money_with_wings: Сумма: <b>{amount} RUB</b>"
)
