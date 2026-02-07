from asyncio import sleep

from aiogram import types
from loguru import logger

from loader import dp, bot_client, config
from models import Worker


@dp.message_handler(commands=["allkick"], admins_chat=True, is_admin=True)
async def kick_all_users(message: types.Message):
    msg = await message.answer("Принял, авторизуюсь.")
    if not bot_client.is_connected:
        authed = await bot_client.connect()
    else:
        await bot_client.disconnect()  # get new con info
        authed = await bot_client.connect()
    if not authed:
        await message.answer("keyerror")
        await bot_client.sign_in_bot(config.api_token)
    offset = 0
    kicked = 0
    workers_chat = config.workers_chat
    while True:
        members = await bot_client.get_chat_members(workers_chat, offset=offset)
        if not members:
            break
        for member in members:
            try:
                if member.status == "member":
                    try:
                        worker = Worker.get(cid=member.user.id)
                        if worker.status == 0:
                            iffsa = await dp.bot.kick_chat_member(
                                workers_chat, member.user.id
                            )
                            if iffsa:
                                kicked += 1
                    except Worker.DoesNotExist:
                        iffsa = await dp.bot.kick_chat_member(
                            workers_chat, member.user.id
                        )
                        if iffsa:
                            kicked += 1
                    await msg.edit_text(f"Исключил: {kicked}")
                    await sleep(0.6)
            except Exception as ex:
                logger.exception(ex)
            await sleep(0.2)
        offset += 1
        await sleep(0.1)
    await msg.reply("Закончил емае!")
