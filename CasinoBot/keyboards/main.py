from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize

from models import User
from data.config import QIWI_ACCOUNTS

# cancel button
cancel_button = KeyboardButton(emojize("Назад :arrow_up:"))

# bot main keyboard
def main_keyboard(chat_id):
	main_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	play_button = KeyboardButton(emojize("Играть :four_leaf_clover:"))
	sup_button = KeyboardButton(emojize("Информация :bulb:"))
	selfcab_button = KeyboardButton(emojize("Личный кабинет :briefcase:"))
	main_keyboard.row(play_button)
	main_keyboard.row(sup_button, selfcab_button)
	
	try:
		user = User.get(cid=chat_id)
		if user.worker:			
			worker_button = KeyboardButton(emojize("Воркер панель :alien:"))
			main_keyboard.row(worker_button)	
	except User.DoesNotExist:
		pass
	
	return main_keyboard

selfcab_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
in_button = KeyboardButton(emojize("Пополнить :moneybag:"))
promo_button = KeyboardButton(emojize("Ввести промокод :key:"))
out_button = KeyboardButton(emojize("Вывести :money_with_wings:"))
selfcab_keyboard.row(in_button, out_button)
selfcab_keyboard.row(promo_button)
selfcab_keyboard.row(cancel_button)

# admin panel keyboard
admin_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
workers_button = KeyboardButton("Воркеры")
paymode_button = KeyboardButton("Смена режима пополнений")
last_button = KeyboardButton("Последние юзеры")
notify_button = KeyboardButton("Оповещение")
qiwi_button = KeyboardButton("Qiwi")
admin_keyboard.add(qiwi_button)
admin_keyboard.add(workers_button, notify_button)
admin_keyboard.add(last_button, paymode_button)
admin_keyboard.add(cancel_button)

admin_work_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
add_worker_button = KeyboardButton("Добавить воркера")
del_worker_button = KeyboardButton("Удалить воркера")
admin_work_keyboard.add(add_worker_button, del_worker_button)
admin_work_keyboard.add(cancel_button)

def welcome_keyboard(ref_id: int):
	welcome_keyboard = InlineKeyboardMarkup()
	accept_button = InlineKeyboardButton(emojize(":white_check_mark: Принять правила"), 
		callback_data=f"accept_{ref_id}")
	welcome_keyboard.add(accept_button)
	return welcome_keyboard

def add_req_keyboard(amount: int, comment: int, number):
	url = f"https://qiwi.com/payment/form/99?currency=RUB&amountInteger={amount}\
	&amountFraction=0&extra['account']={number}&extra['comment']={comment}" 

	markup = InlineKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
	goto_button = InlineKeyboardButton(emojize("Перейти к оплате :arrow_heading_up:"), url=url) 
	check_button = InlineKeyboardButton(emojize("Проверить оплату :recycle:"), callback_data=f"check_{comment}_{number}") 
	markup.add(goto_button, check_button)

	return markup

qiwi_keyboard = InlineKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
for acc in QIWI_ACCOUNTS:
	qiwi_keyboard.add(InlineKeyboardButton(acc, callback_data=f"qiwi_{acc}"))


def payment_done_keyboard(cid, comment):
	markup = InlineKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	accept_button = InlineKeyboardButton(emojize("Пополнить :sparkle:"), callback_data=f"done_{cid}_{comment}")
	markup.add(accept_button)
	return markup

# admin panel keyboard
notify_keyboard = InlineKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
sure_button = InlineKeyboardButton("Sure", callback_data="sure")
notify_keyboard.add(sure_button)
