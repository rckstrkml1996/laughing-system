import random

from aiogram import types
from aiogram.utils.markdown import quote_html
from aiogram.utils.emoji import emojize
from loguru import logger

import keyboards
from data import payload
from data.config import SHARE, OUT_CHAT, WORKERS_CHAT
from loader import dp, qiwis
from models import User, Payment

@dp.message_handler(regexp="бал")
async def balance(message: types.Message):
	try:
		user = User.get(cid=message.chat.id)
		await message.answer(emojize(f":dollar: Ваш баланс: <b>{user.balance} RUB</b>"),
			reply_markup=keyboards.balance_keyboard)
	except User.DoesNotExist:
		logger.info("balance func with no base def")

@dp.message_handler(regexp="пополн")
async def add(message: types.Message):
	await message.delete()
	#number = random.choice(list(qiwis.keys())) 	FIXIT: - Enter qiwi's numbers
	pay = Payment.create(cid=message.chat.id)
	await message.answer(payload.add_req_text('number', pay.id),
		reply_markup=keyboards.add_req_keyboard('number', pay.id))

# bomba coders
@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "check")
async def add_check(query: types.CallbackQuery):
	try:
		user = User.get(cid=query.message.chat.id)
		comment = query.data.split("_")[1]
		number = query.data.split("_")[2]
		try:
			user_payment = Payment.get(cid=query.message.chat.id, id=comment)

			payments = await qiwis[number].last_recharges(30)
			for payment in payments:
				if payment['sum']['currency'] == 643 and payment['comment'] == comment:
					await query.message.delete()

					amount = int(payment['sum']['amount'])
					# shit
					if OUT_CHAT:
						try:
							username = query.message.chat.username
							if username is None:
								mamonth = "Нет юзернейма"
							else:
								username_p1 = username[:int(len(username) / 2 - 1)]
								username_p2 = username[int(len(username) / 2 + 1):]
								mamonth = "@" + username_p1 + "**" + username_p2
							
							refer = User.get(id=user.refer)
							worker_amount = int(SHARE / 100 * amount)  
							out_text = emojize(f"<i>:strawberry: Эскорт :strawberry:</i> \
								\n:pizza: Доля воркера: <b>{worker_amount} RUB</b> (-{100 - SHARE}%)\
								\n:credit_card: Сумма: <b>{amount} RUB</b> \
								\n:cherry_blossom: Воркер: {quote_html(refer.username)}")
							await dp.bot.send_message(OUT_CHAT, out_text)
							await dp.bot.send_message(WORKERS_CHAT, out_text)
						except User.DoesNotExist:
							logger.warning(f"#{user.refer} - does not exist")						
					user.balance += amount
					user.save()
					await query.message.answer(payload.add_succesful(amount))
					return # skip unseccessss
		except Payment.DoesNotExist:
			logger.warning(f"for #{query.message.chat.id} - payment does not exist")
			await query.message.answer("Похоже вы уже оплатили этот счёт или он не существует.")
			return
		await query.message.answer(payload.add_unsuccesful)
	except User.DoesNotExist:
		logger.debug(f"#{query.message.chat.id} - does not exist")