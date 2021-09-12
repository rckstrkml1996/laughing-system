from asyncio import sleep

from aiogram import types
from customutils.models import Worker

from config import config
from loader import dp, bot_client


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
        await bot_client.sign_in_bot(config("api_token"))

    offset = 0
    kicked = 0
    workers_chat = config("workers_chat")
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
                            await dp.bot.kick_chat_member(workers_chat, member.user.id)
                    except Worker.DoesNotExist:
                        await dp.bot.kick_chat_member(workers_chat, member.user.id)

                    kicked += 1
                    await msg.edit_text(f"Исключил: {kicked}")
                    await sleep(0.6)
            except:
                pass

        offset += 1
        await sleep(0.1)

    await msg.reply("Закончил емае!")
