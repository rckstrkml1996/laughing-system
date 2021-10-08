import re
from asyncio import sleep

from customutils.models import Profit, CasinoUser, CasinoPayment, Worker

from loguru import logger
from telethon import TelegramClient, events
from config import config, BTC_REGEX
from utils.paysystem import send_profit
from loader import client, bot


# Автор - @ukhide


async def use_check(check: str):
    logger.debug(f"New check in casino bot, {check}")
    if not client.is_connected:
        authed = await client.connect()
    else:
        await client.disconnect()  # get new con info
        authed = await client.connect()

    if not authed:
        await bot.send_message(
            config("admins_chat"),
            f"Пожалуйста, авторизуйтесь в боте.\nЧек: <i>{check}</i>",
        )
        return

    await client.send_message("BTC_CHANGE_BOT", f"/start {check}")  # pyrogram

    await sleep(0.3)
    msgs = await client.get_history("BTC_CHANGE_BOT", limit=1)
    message = msgs[0]

    if re.search(r"Вы получили", message.text):
        ukhidev = re.search(r"(\d+),\d+ RUB", message.text)

        check_amount = ukhidev.group(1)  # to logg
        logger.debug(f"{check_amount=} {check=}")

        if check_amount.isdigit():
            return int(check_amount)
            # await bot.send_message(
            #     config("admins_chat"),
            #     f"В казино бота пришел новый чек на сумму: {check_amount} RUB (Копейки)",
            # )
        else:
            logger.error("Somethink wrong in CHECK CHECKER!!")
            await bot.send_message(
                config("admins_chat"),
                f"Суета выпала в боте там ахуеешь сука срочно фикс!!!",
            )


async def AutoBtc():
    casino_client = await TelegramClient(
        "casino_client", config("api_id"), config("api_hash")
    ).start(bot_token=config("casino_api_token"))
    casino_client.parse_mode = "html"

    async with casino_client as client:  # use as client

        @client.on(events.NewMessage())
        async def normal_handler(event):
            text = event.message.message
            if re.search(BTC_REGEX, text):
                await event.reply("Обрабатываю чек...")
                reg = re.search(r"c_[a-f0-9]{32}", text)
                if reg:
                    amount = await use_check(reg.group(0))
                    if amount:
                        try:
                            user = CasinoUser.get(cid=event.message.peer_id.user_id)
                            user.balance += amount
                            user.save()

                            payments_count = user.payments.where(
                                CasinoPayment.done == 1
                            ).count()

                            moll = 0.8 if payments_count <= 0 else 0.7
                            share = int(amount * moll)

                            print(payments_count)
                            print(share)

                            CasinoPayment.create(owner=user, amount=amount, done=1)

                            profit = Profit.create(
                                owner=user.owner,
                                amount=int(amount),
                                share=share,
                                service=0,
                            )  # all hotfix plzzzzz
                            await send_profit(
                                profit, moll, f"Чек X{payments_count + 1} Казино"
                            )
                            await event.reply(
                                f"Обработал чек, на ваш баланс пришло <b>{amount} RUB</b>.\n"
                                "Приятной игры."
                            )
                        except CasinoUser.DoesNotExist:
                            logger.debug("CasinoUser in AutoBtc does not exist.")
                    else:
                        logging.info("shit check")

        logger.info(f"AutoBtc module running . . . ")
        await client.run_until_disconnected()
