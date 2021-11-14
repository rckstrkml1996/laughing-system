from loguru import logger

from loader import config, casino_bot, escort_bot, trading_bot
from customutils import save_config


async def update_bot_usernames():
    casino_username = config.casino_username
    escort_username = config.escort_username
    trading_username = config.trading_username

    casino_user = await casino_bot.get_me()
    new_casino_username = casino_user.username
    await casino_bot.session.close()

    escort_user = await escort_bot.get_me()
    new_escort_username = escort_user.username
    await escort_bot.session.close()

    trading_user = await trading_bot.get_me()
    new_trading_username = trading_user.username
    await trading_bot.session.close()

    if casino_username != new_casino_username:
        config.casino_username = new_casino_username
        logger.info(
            f"Updated old {casino_username=} in config to {new_casino_username}"
        )
    if escort_username != new_escort_username:
        config.escort_username = new_escort_username
        logger.info(
            f"Updated old {escort_username=} in config to {new_escort_username}"
        )
    if trading_username != new_trading_username:
        config.trading_username = new_trading_username
        logger.info(
            f"Updated old {trading_username=} in config to {new_trading_username}"
        )

    save_config(config)
