from aiogram.types import CallbackQuery, Message

from loader import dp


@dp.callback_query_handler(is_user=False)
async def not_user_cb(query: CallbackQuery):
    await query.answer("Ты не юзер бота!")


@dp.message_handler(is_user=False)
async def not_user_msg(message: Message):
    await message.answer("Ты не юзер бота!")  # my be delete
