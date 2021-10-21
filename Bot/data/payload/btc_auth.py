from aiogram.utils.emoji import emojize



btc_authed_text = emojize(
    "<i>Авторизовался!</i> :cold_face:\n" "Имя: <b>{name}</b>\n" "Юзернейм: @{username}"
)

check_true_text = emojize(
    ":ok_hand: <b>Успешно</b> обналичил этот чек!\n" "Сумма: <b>+{amount} ?RUB?</b>\n"
)

btc_log_out_success = emojize(":white_check_mark: Вышел успешно!")

btc_log_out_invalid = emojize(":warning: Не вышел!")
