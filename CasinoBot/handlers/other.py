from aiogram import types
from aiogram.types import ChatType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from aiogram.utils.emoji import emojize
from loguru import logger

from loader import dp
from models import User
from .main import main_menu


""" for all states """
@dp.message_handler(chat_type=ChatType.PRIVATE, commands=["top", "workers"], state="*")
@dp.message_handler(Text(startswith="топ", ignore_case=True), 
	chat_type=ChatType.PRIVATE, state="*")
async def top_workers_in_bot(message: types.Message):
	return

@dp.message_handler(commands=["top", "workers"], state="*")
@dp.message_handler(Text(startswith="топ", ignore_case=True), state="*")
async def top_workers(message: types.Message):
	top_workers_text = emojize("Топ Воркеров Hide Team :snake:")
	for worker in User.select().where(User.worker).order_by(User.ref_balance.desc()).limit(25):
		top_workers_text += f"\n{worker.username} - {round(worker.ref_balance / 0.75, 1)}₽"
	await message.answer(top_workers_text)


@dp.message_handler(commands=["start"], state="*")
async def hello_bro(message: types.Message):
	await message.answer("шо надо?")

@dp.message_handler(chat_type=ChatType.PRIVATE, state='*', commands='cancel')
@dp.message_handler(Text(startswith='закон', ignore_case=True), 
	chat_type=ChatType.PRIVATE, state='*')
@dp.message_handler(Text(startswith='назад', ignore_case=True), 
	chat_type=ChatType.PRIVATE, state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
	"""
	Allow user to cancel any action
	/cancel или нач. - закон, назад - завершение любого стейта
	"""
	current_state = await state.get_state()
	if current_state is None:
		await main_menu(message, state)
		return

	logger.info(f'Cancelling state {current_state}')

	await state.finish()
	await main_menu(message, state)

@dp.message_handler(content_types=["new_chat_members"])
async def handler_new_member(message: types.Message):
	user_name = message.chat.username
	if user_name is None:
		user_name = message.new_chat_members[0].first_name
	await message.answer(emojize(f"Добро пожаловать, {user_name}! \
		\n<a href='https://t.me/c/1177185268/294491'>ЗАКРЕП</a>, Удачи :four_leaf_clover:"))