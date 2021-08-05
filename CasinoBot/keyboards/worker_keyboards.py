from random import choice

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

from models import User

main_menu_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
about_user_button = KeyboardButton(emojize("О юзере :eyes:"))
edit_balance_button = KeyboardButton(emojize("Изменить баланс :smiling_imp:"))
notify_button = KeyboardButton(emojize("Сообщение :love_letter:"))
cancel_button = KeyboardButton(emojize("Назад :arrow_up:"))
main_menu_keyboard.add(about_user_button, edit_balance_button, notify_button)
main_menu_keyboard.add(cancel_button)

edit_balance_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
worker_menu = KeyboardButton(emojize("Воркер меню :poop:"))
edit_balance_keyboard.add(worker_menu)

def status_keyboard_pos(cid):
	markup = InlineKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
	status_pos = InlineKeyboardButton(emojize("Cтатус :white_check_mark:"),
									callback_data=f"status_{cid}")
	update = InlineKeyboardButton(emojize("Обновить :recycle:"),
								callback_data=f"update_{cid}")
	markup.add(status_pos, update)
	return markup

def status_keyboard_neg(cid):
	markup = InlineKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
	status_neg = InlineKeyboardButton(emojize("Cтатус :negative_squared_cross_mark:"),
									callback_data=f"status_{cid}")
	update = InlineKeyboardButton(emojize("Обновить :recycle:"),
								callback_data=f"update_{cid}")
	markup.add(status_neg, update)
	return markup

refers_smiles = [":elephant:", ":shark:", ":pig2:"]

def last_refers(cid):
	markup = InlineKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	for refer in User.select().where(User.refer == cid).order_by(User.id.desc()).limit(3):
		markup.add(InlineKeyboardButton(emojize(f"{refer.fullname} {choice(refers_smiles)}"),
										callback_data=f"update_{refer.cid}"))
	return markup

notify_sure = InlineKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
sure_button = InlineKeyboardButton(emojize("Уверен! :warning:"),
								callback_data="notify")
notify_sure.add(sure_button)