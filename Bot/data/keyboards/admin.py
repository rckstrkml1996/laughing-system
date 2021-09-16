from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


def summary_check_keyboard(chat_id):
    markup = InlineKeyboardMarkup()
    accept_btn = InlineKeyboardButton(
        emojize(":white_check_mark: Принять"), callback_data=f"accept_{chat_id}"
    )
    reject_btn = InlineKeyboardButton(
        emojize(":warning: Отклонить"), callback_data=f"reject_{chat_id}"
    )
    block_btn = InlineKeyboardButton(
        emojize(":no_entry_sign: Заблокировать"), callback_data=f"block_{chat_id}"
    )
    markup.add(accept_btn)
    markup.add(reject_btn, block_btn)

    return markup


def admworkstatus_keyboard(work_stat, casino_stat, escort_stat, trading_stat):
    markup = InlineKeyboardMarkup()

    change_work_btn = InlineKeyboardButton(
        emojize(
            ":full_moon: Сменить статус" if work_stat else ":new_moon: Сменить статус"
        ),
        callback_data="toggle_status",
    )
    change_casino_btn = InlineKeyboardButton(
        emojize(":full_moon: Казино" if casino_stat else ":new_moon: Казино"),
        callback_data="toggle_casino_status",
    )
    change_escort_btn = InlineKeyboardButton(
        emojize(":full_moon: Эскорт" if escort_stat else ":new_moon: Эскорт"),
        callback_data="toggle_escort_status",
    )
    change_trading_btn = InlineKeyboardButton(
        emojize(":full_moon: Трейдинг" if trading_stat else ":new_moon: Трейдинг"),
        callback_data="toggle_trading_status",
    )

    markup.add(change_casino_btn)
    markup.add(change_escort_btn, change_trading_btn)
    markup.add(change_work_btn)

    return markup


# /pin command
change_pin_keyboard = InlineKeyboardMarkup()
changeit_btn = InlineKeyboardButton(
    emojize(":pencil2: Изменить закреп"), callback_data="change_pin"
)
change_pin_keyboard.add(changeit_btn)

new_pin_keyboard = InlineKeyboardMarkup()
newpin_btn = InlineKeyboardButton(
    emojize(":white_check_mark: Сохранить изменения"), callback_data="savepin"
)
oldpin_btn = InlineKeyboardButton(
    emojize(":x: Не сохранять"), callback_data="unsavepin"
)
new_pin_keyboard.add(newpin_btn)
new_pin_keyboard.add(oldpin_btn)

# /qiwi command
add_qiwi_keyboard = InlineKeyboardMarkup()
add_qiwi_btn = InlineKeyboardButton(
    emojize("Добавить киви :information_source:"), callback_data="add_qiwi"
)
add_qiwi_keyboard.add(add_qiwi_btn)


def qiwi_keyboard(accounts: list):
    markup = InlineKeyboardMarkup()

    for i, acc in enumerate(accounts):
        if i == 0:
            markup.add(
                InlineKeyboardButton(
                    emojize(f"{acc} :sparkle:"), callback_data=f"qiwi_{i}"
                )
            )
        else:
            markup.add(InlineKeyboardButton(acc, callback_data=f"qiwi_{i}"))

    markup.add(add_qiwi_btn)

    return markup


def oneqiwi_keyboard(num):
    markup = InlineKeyboardMarkup()

    add_proxy_btn = InlineKeyboardButton(
        emojize("Добавить прокси :diamond_shape_with_a_dot_inside:"),
        callback_data=f"addproxy_{num}",
    )
    delete_qiwi_btn = InlineKeyboardButton(
        emojize("Удалить :x:"), callback_data=f"qiwidelete_{num}"
    )
    back_btn = InlineKeyboardButton("Назад", callback_data="backqiwi")

    markup.add(add_proxy_btn)
    markup.add(delete_qiwi_btn)
    markup.add(back_btn)

    return markup


def qiwi_delete_keyboard(num):
    markup = InlineKeyboardMarkup()
    sure_btn = InlineKeyboardButton(
        emojize("Уревенрбялдь уверен нахуй :wastebasket:"),
        callback_data=f"suredelete_{num}",
    )
    markup.add(sure_btn)
    markup.add(cancel_btn)

    return markup


# /alert command
alert_keyboard = InlineKeyboardMarkup()
alert_bot_btn = InlineKeyboardButton(
    emojize("Основной бот :robot:"), callback_data="alert_bot"
)
alert_casino_bots_btn = InlineKeyboardButton(
    emojize("Казино :slot_machine:"), callback_data="alert_casino"
)
alert_escort_bots_btn = InlineKeyboardButton(
    emojize("Эскорт :strawberry:"), callback_data="alert_escort"
)
alert_trading_bot_btn = InlineKeyboardButton(
    emojize("Трейдинг :chart_with_upwards_trend:"), callback_data="alert_trading"
)
alert_keyboard.add(alert_bot_btn)
alert_keyboard.add(alert_casino_bots_btn)
alert_keyboard.add(alert_escort_bots_btn, alert_trading_bot_btn)


alert_accept_keyboard = InlineKeyboardMarkup()
alert_accept_btn = InlineKeyboardButton(
    emojize(":white_check_mark: Подтвердить"), callback_data="alert_accept"
)
alert_edit_btn = InlineKeyboardButton(
    emojize(":pencil2: Изменить"), callback_data="alert_edit"
)
alert_reject_btn = InlineKeyboardButton(
    emojize(":x: Отменить"), callback_data="alert_reject"
)
alert_accept_keyboard.add(alert_accept_btn)
alert_accept_keyboard.add(alert_edit_btn, alert_reject_btn)

serv_alaccept_keyboard = InlineKeyboardMarkup()
serv_alaccept_keyboard.add(alert_accept_btn)


# /sys command
update_sysinfo_keyboard = InlineKeyboardMarkup()
sys_info_update_btn = InlineKeyboardButton(
    emojize(":arrows_counterclockwise:"), callback_data="update_sys"
)
sys_restart_btn = InlineKeyboardButton(
    emojize("Перезагрузить сервер"), callback_data="restart_sys"
)
code_restart_btn = InlineKeyboardButton(
    emojize("Перезапустить бота"), callback_data="restart_code"
)
update_sysinfo_keyboard.add(sys_info_update_btn)
update_sysinfo_keyboard.add(code_restart_btn, sys_restart_btn)


# on new profit
def profit_pay_keyboard(prft_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    pay_btn = InlineKeyboardButton(
        emojize("Выплатить :white_check_mark:"), callback_data=f"truepay_{prft_id}"
    )
    dontpay_btn = InlineKeyboardButton(
        emojize("Заморозка! :cold_face:"), callback_data="freeze"
    )
    markup.add(pay_btn)
    markup.add(dontpay_btn)

    return markup
