from os import getenv

from dynaconf import Dynaconf
from loguru import logger

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['../settings.toml', '../.secrets.toml'],
)  # ты далбаеб создавай у себя файл .secrets.toml в главной папке ебаа


# API_TOKEN = getenv("BOT_TOKEN")  # взятие токена из переменной среды
# REQ_TOKEN = ""

if not settings.CAS_API_TOKEN:  # если вы не указали токен бота
    logger.error("Please specify the bot token... env variable - BOT_TOKEN")

# или же тупо вставить сюда не из переменной среды
# ADMINS_ID = [904164632, 1404657362, 1485049507, ]

# DATABASE_FILE = "base.db"  # имя файла базы данных

# SHARE = 75  # дефолтный процент для воркеров
MINIK = 150  # минимальная сумма пополнения

LICENCE = "AgACAgIAAxkBAAEOOY1gU9f3uRanl2h-YCVh3PFbprQWLQACN7QxG2NPoUrQtlfP33-xv-Tzk6IuAAMBAAMCAAN5AAMgBgACHgQ"

# Сюда фейк вывод
# FAKE_NUMBER = "79603377491"
# Если True - Бот принимает платежи на автомате
# PAYMENTS_MODE = True  # Автомат/Ручка

OUT_CHAT = "@hideteamout"  # если None - не куда
WORKERS_CHAT = "-1001177185268"
SUP = "XbetCasino_Support"  # без @
LIFE_OUTS = "@XbetCasino_Outs"

# for qiwi payments
# QIWI_TOKENS = getenv("QIWI_TOKENS")
if not settings.CAS_QIWI_TOKENS:
    logger.error("Please specify the qiwi token... env variable - QIWI_TOKENS")
# else:
    # QIWI_TOKENS = [x for x in QIWI_TOKENS.split(";") if x]  # среда

# QIWI_ACCOUNTS = getenv("QIWI_ACCOUNTS")
if not settings.CAS_QIWI_ACCOUNTS:
    logger.error(
        "Please specify the qiwi token... env variable - QIWI_ACCOUNTS")
else:
    # QIWI_ACCOUNTS = [x for x in QIWI_ACCOUNTS.split(
    # ";") if x]  # пополнение в боте - сюда
    if len(QIWI_TOKENS) != len(QIWI_ACCOUNTS):
        logger.error("Value of tokens dont suply value of numbers")

# Количество выводимых последних пополнений) ();К!)
PAY_ROWS = 12

SKIP_UPDATES = True  # если бот был выключен, а в этот момент
# кто то писал ему, то после включения он проигнорит эти сообщения

# Промокоды и их сумма
PROMOS = {"CHH50": 500, "2FA5D": 250, "SA15D": 150}

# Все круто!
logger.debug("Config setup succes!")
