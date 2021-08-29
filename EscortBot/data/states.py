from aiogram.dispatcher.filters.state import State, StatesGroup

'''
	Все это стоит проигнорировать, это стейты - такая штука
	Которая переводит из одного состояния отношений с юзером в другое

	Пример:
		1 - Играть - Любое сообщение |
		2 - Ставка - |" Ставка сохранилась в стейт и тд.
'''

class GirlsChoice(StatesGroup):
	main = State()
	order = State()

class EnterPromo(StatesGroup):
    waiting_promo = State()
    
class EnterKey(StatesGroup):
    main = State()