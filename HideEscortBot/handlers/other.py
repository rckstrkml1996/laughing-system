from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from loguru import logger

from loader import dp
from .main import welcome


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(startswith='верну', ignore_case=True), state='*')
@dp.message_handler(Text(startswith='наз', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
	"""
	Allow user to cancel any action
	/cancel или нач. - закон, назад - завершение любого стейта
	"""
	current_state = await state.get_state()
	if current_state is None:
		await welcome(message, state)
		return

	logger.info(f'Cancelling state {current_state}')

	await state.finish()
	await welcome(message, state)
