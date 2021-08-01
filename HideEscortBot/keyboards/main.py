from random import shuffle

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, callback_query
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


main_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
girls_btn = KeyboardButton("🦋 Анкеты")
balance_btn = KeyboardButton("💰 Баланс")
support_btn = KeyboardButton("👨‍💻 Поддержка")
garanties_btn = KeyboardButton("🔐 Гарантии")
promo_btn = KeyboardButton("🤑 Промокод")
main_keyboard.add(girls_btn, balance_btn, garanties_btn, promo_btn, support_btn)

balance_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
add_btn = KeyboardButton("💸 Пополнить")
back_btn = KeyboardButton("⬅️ Назад")
balance_keyboard.add(add_btn, back_btn)

def add_req_keyboard(number, comment):
	url = f"https://qiwi.com/payment/form/99?currency=RUB&amountInteger=1500\
	&amountFraction=0&extra['account']={number}&extra['comment']={comment}" 

	markup = InlineKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
	goto_button = InlineKeyboardButton(emojize("Перейти к оплате :arrow_heading_up:"), url=url) 
	check_button = InlineKeyboardButton(emojize("Проверить оплату :recycle:"), callback_data=f"check_{comment}_{number}") 
	markup.add(goto_button, check_button)

	return markup

emojis = [
	":crown:", ":ring:", ":gem:", ":heart:",
	":black_heart:", ":sparkling_heart:", ":cat:",
	":new_moon_with_face:", ":cherry_blossom:", ":rose:",
	":star:", ":rainbow:", ":sweat_drops:", ":kiss:"
]

def girl_choice_keyboard(num):
	markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

	if len(emojis) < num:
		logger.error("Emojis lower than girls num")
		return None
	shuffle(emojis)
	buttons = []
	for i in range(num):
		buttons.append(KeyboardButton(emojize(f"{emojis[i]} Номер {i + 1}")))
	markup.add(*buttons)
	markup.add(back_btn)
	
	return markup

order_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
order_btn = KeyboardButton(emojize("Заказать :white_check_mark:"))
order_keyboard.add(order_btn, back_btn)

promo_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
promo_keyboard.add(back_btn)