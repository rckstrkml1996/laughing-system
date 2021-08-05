from aiogram.dispatcher.filters.state import State, StatesGroup

'''
	Все это стоит проигнорировать, это стейты - такая штука
	Которая переводит из одного состояния отношений с юзером в другое

	Пример:
		1 - Играть - Любое сообщение |
		2 - Ставка - |" Ставка сохранилась в стейт и тд.
'''

class AdminPanel(StatesGroup):
	main = State()
	qiwi_out = State()
	workers = State()
	workers_add = State()
	workers_delete = State()
	notify = State()
	notify_sure = State()

class WorkerPanel(StatesGroup):
	main = State()
	edit_balance_id = State()
	edit_balance_amount = State()
	notify_id = State()
	notify_text = State()
	notify_sure = State()
	about_user = State()

class Game(StatesGroup):
	chose_game = State()
	casino_anymes = State()
	casino_stake = State()
	casino_bet = State()
	dice_anymes = State()
	dice_stake = State()

class SelfCabine(StatesGroup):
	main = State()

class AddBalance(StatesGroup):
	amount = State()

class OutBalance(StatesGroup):
	amount = State()
	number = State()
	promo = State()
