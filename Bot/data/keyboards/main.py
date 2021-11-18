from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

# worker panel
menu_keyboard = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
profile_btn = KeyboardButton(emojize("Профиль :cold_face:"))
casino_btn = KeyboardButton(emojize("Казик :slot_machine:"))
trading_btn = KeyboardButton(emojize("Трейдинг :chart:"))
escort_btn = KeyboardButton(emojize("Эскорт :green_heart:"))
about_btn = KeyboardButton(emojize("О проекте :man_technologist:"))
menu_keyboard.add(profile_btn)
menu_keyboard.add(trading_btn, casino_btn, escort_btn)
menu_keyboard.add(about_btn)


render_btn = InlineKeyboardButton(
    emojize("Отрисовка :receipt:"),
    callback_data="render",
)


def panel_keyboard(namehide) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    username_btn = InlineKeyboardButton(
        f'{"Открыть" if namehide else "Скрыть"} никнейм в выплатах',
        callback_data="toggleusername",
    )
    markup.add(username_btn)
    markup.add(render_btn)

    return markup


def about_project_keyboard(
    outs_link: str,
    reviews_link: str,
    workers_link: str,
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    ref_btn = InlineKeyboardButton(
        emojize("Реф. система :handshake: "), callback_data="refsystem"
    )
    rules_btn = InlineKeyboardButton(
        emojize("Правила :scroll: "), callback_data="showrules"
    )
    out_btn = InlineKeyboardButton(
        emojize("Выплаты :money_with_wings:"), url=f"t.me/{outs_link}"
    )
    info_btn = InlineKeyboardButton(
        emojize("Инфоканал :wastebasket:"), url=f"t.me/{reviews_link}"
    )
    chat_btn = InlineKeyboardButton(
        emojize("Чат воркеров :hot_face:"),
        url=f"https://t.me/joinchat/{workers_link}",
    )
    markup.add(ref_btn, rules_btn)
    markup.add(info_btn, out_btn)
    markup.add(chat_btn)

    return markup
