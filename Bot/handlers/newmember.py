from aiogram import types

from loader import dp
from data.payload import new_chat_member_text


@dp.message_handler(content_types=["new_chat_members"], workers_chat=True)
async def new_chat_member(message: types.Message):
    bot_user = await dp.bot.get_me()
    await message.reply(
        new_chat_member_text.format(
            chat_id=message.from_user.id,
            name=message.from_user.full_name,
            bot_username=bot_user.username,
        )
    )
