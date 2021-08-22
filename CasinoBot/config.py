# from os import getenv

from loguru import logger

from customutils.confparse import Config

config = Config("Settings", "../config.cfg", {})

# # API_TOKEN = getenv("BOT_TOKEN")  # взятие токена из переменной среды
# # REQ_TOKEN = ""

# CAS_API_TOKEN = "1654386645:AAG1siaWQE8hN-jL6eXmLgd75R5MFcGc_UU"

# if not CAS_API_TOKEN:  # если вы не указали токен бота
#     logger.error("Please specify the bot token... env variable - BOT_TOKEN")

# # или же тупо вставить сюда не из переменной среды
# # ADMINS_ID = [904164632, 1404657362, 1485049507, ]

# # DATABASE_FILE = "base.db"  # имя файла базы данных

# SHARE = 75  # дефолтный процент для воркеров
MINIK = 150  # минимальная сумма пополнения

LICENCE = "AgACAgIAAxkBAAEOOY1gU9f3uRanl2h-YCVh3PFbprQWLQACN7QxG2NPoUrQtlfP33-xv-Tzk6IuAAMBAAMCAAN5AAMgBgACHgQ"

# # Сюда фейк вывод
# # FAKE_NUMBER = "79603377491"
# # Если True - Бот принимает платежи на автомате
PAYMENTS_MODE = True  # Автомат/Ручка

# OUT_CHAT = "@hideteamout"  # если None - не куда
# WORKERS_CHAT = "-1001177185268"
# SUP = "XbetCasino_Support"  # без @
# LIFE_OUTS = "@XbetCasino_Outs"

# CAS_QIWI_TOKENS = "7772212221321321321312321"
# CAS_QIWI_ACCOUNTS = "77777777779"
# # for qiwi payments
# # QIWI_TOKENS = getenv("QIWI_TOKENS")
# if not CAS_QIWI_TOKENS:
#     logger.error("Please specify the qiwi token... env variable - QIWI_TOKENS")
# # else:
#     # QIWI_TOKENS = [x for x in QIWI_TOKENS.split(";") if x]  # среда

# # QIWI_ACCOUNTS = getenv("QIWI_ACCOUNTS")
# if not CAS_QIWI_ACCOUNTS:
#     logger.error(
#         "Please specify the qiwi token... env variable - QIWI_ACCOUNTS")
# else:
#     # QIWI_ACCOUNTS = [x for x in QIWI_ACCOUNTS.split(
#     # ";") if x]  # пополнение в боте - сюда
#     if len(CAS_QIWI_TOKENS) != len(CAS_QIWI_ACCOUNTS):
#         logger.error("Value of tokens dont suply value of numbers")

# # Количество выводимых последних пополнений) ();К!)
# PAY_ROWS = 12

SKIP_UPDATES = True  # useless

# # Промокоды и их сумма
# PROMOS = {"CHH50": 500, "2FA5D": 250, "SA15D": 150}

# # Все круто!
# logger.debug("Config setup succes!")
