from os import getenv

from loguru import logger


API_TOKEN = '1903661646:AAGI7lXnEJ11ljzDPNnN0NPMwD9FTB9vv64'

DATABASE_FILE = "base.db" # имя файла базы данных

SHARE = 80

OUT_CHAT = "@hideteamout" # если None - не куда
WORKERS_CHAT = "-1001177185268"
SUP = "butterfly_sup" # без @
OTZ = "btrfly_otz" # без @

PROMOS = { "cfg500":500, "gzk200":200, "bvn100":100 }

VIDEO_ID = "BAACAgIAAxkBAAIDwWBgSMaftZ8LXh1T_lnROP7LX7F-AAINDAACvAoAAUtvlt1Xy138zR4E"
# video id - garanties vid id
ADMINS_ID = [1672987695]

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

SKIP_UPDATES = True # если бот был выключен, а в этот момент

logger.debug(" setup succes!")
