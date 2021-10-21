from aiogram import Bot
from loguru import logger

from config import config
from loader import casino_bot, escort_bot, trading_bot


async def update_bot_usernames():
    casino_username = config("casino_username")
    escort_username = config("escort_username")
    trading_username = config("trading_username")

    casino_user = await casino_bot.get_me()
    new_casino_username = casino_user.username
    escort_user = await escort_bot.get_me()
    new_escort_username = escort_user.username
    trading_user = await trading_bot.get_me()
    new_trading_username = trading_user.username

    usernames_good = True

    if casino_username != new_casino_username:
        usernames_good = False
        config.edit("casino_username", new_casino_username)
        logger.debug(
            f"Updated old {casino_username=} in config.cfg to {new_casino_username}"
        )

    if escort_username != new_escort_username:
        usernames_good = False
        config.edit("escort_username", new_escort_username)
        logger.debug(
            f"Updated old {escort_username=} in config.cfg to {new_escort_username}"
        )

    if trading_username != new_trading_username:
        usernames_good = False
        config.edit("trading_username", new_trading_username)
        logger.debug(
            f"Updated old {trading_username=} in config.cfg to {new_trading_username}"
        )

    if usernames_good:
        logger.debug("Casino Escort Trading bots usernames is correct!")
