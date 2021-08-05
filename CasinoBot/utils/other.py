import asyncio
from random import randint

from loguru import logger
from aiogram import Bot
from aiogram.utils.emoji import emojize

from data.config import LIFE_OUTS

def generate():
	nose = randint(0, 1)
	last_out = randint(333, 33333)
	sxll = last_out % 100 if nose else 0
	last_out -= sxll
	return last_out

def ru_out():
	number_out =  f"Номер QIWI: <b>+79*****{randint(1111, 9999)}</b> :kiwi_fruit: " if randint(1, 2) == 1 \
		else f"Номер карты: <b>{randint(4, 5)}*** **** **** **{randint(11, 49)}</b> :credit_card: "

	return emojize(f":money_with_wings: Успешный вывод средств! \
	\n\nСумма вывода: <b>{generate()} RUB</b> :moneybag: \
	\n{number_out} \
	\nАккаунт верифицирован :white_check_mark:")

def kz_out():
	number_out =  f"Номер QIWI: <b>+779*****{randint(1111, 9999)}</b> :kiwi_fruit: " if randint(1, 2) == 1 \
		else f"Номер карты: <b>{randint(4, 5)}*** **** **** **{randint(11, 49)}</b> :credit_card: "

	return emojize(f":moneybag: Успешный вывод средств! \
	\n\nСумма вывода: <b>{generate()} TENGE</b> :moneybag: \
	\n{number_out} \
	\nАккаунт верифицирован :white_check_mark:")

async def life_outs(bot: Bot):
	while True:
		func = ru_out if randint(1, 100) > 13 else kz_out
		await bot.send_message(LIFE_OUTS, func())
		time = randint(90, 860)
		logger.info(f"life out sleep for {time}s")
		await asyncio.sleep(time)
