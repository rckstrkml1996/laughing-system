from os import getenv
from loguru import logger


API_TOKEN = "1918772845:AAEhg3PiH6u7ElEmQ4_GP_4OuAPyrGCmIBk"

SKIP_UPDATES = True

ADMINS_ID = [1644048831]

MIN_WITHDRAW = 800
MIN_DEPOSIT = 300

QIWI_TOKENS = getenv("QIWI_TOKENS")
if not QIWI_TOKENS:
	logger.error("Please specify the qiwi token... env variable - QIWI_TOKENS")
else:
	QIWI_TOKENS = [x for x in QIWI_TOKENS.split(";") if x] # среда

QIWI_ACCOUNTS = getenv("QIWI_ACCOUNTS")
if not QIWI_ACCOUNTS:
	logger.error("Please specify the qiwi token... env variable - QIWI_ACCOUNTS")
else:
	QIWI_ACCOUNTS = [x for x in QIWI_ACCOUNTS.split(";") if x] # пополнение в боте - сюда
	if len(QIWI_TOKENS) != len(QIWI_ACCOUNTS):
		logger.error("Value of tokens dont suply value of numbers")

logger.debug("Setup succes!")
