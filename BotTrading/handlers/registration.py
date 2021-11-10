from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from loader import dp, main_bot
from data import texts, keyboards
from data.states import Registration
from models import TradingUser, Worker
from .profile import profile  # profile handler


async def create_user(worker: Worker, message: types.Message):
    try:
        user = TradingUser.get(cid=message.chat.id)
    except TradingUser.DoesNotExist:
        user = TradingUser.create(
            owner=worker,
            cid=message.chat.id,
            fullname=message.chat.full_name,
            username=message.chat.username,
        )
        await main_bot.send_message(
            worker.cid,
            texts.main_new_user.format(
                mention=texts.mention_text.format(user_id=user.cid, text=user.fullname),
                user_id=user.id,
            ),
        )

    await profile(message, user)


@dp.message_handler(commands=["start"], is_user=False, state="*")
async def start_new_user(message: types.Message):
    data = message.text.split(" ")
    bot_user = await dp.bot.get_me()
    if len(data) >= 2:
        uniq_key = data[1]
        worker = Worker.get(uniq_key=uniq_key)
        await message.answer(
            texts.rules.format(
                name=message.chat.full_name,
                bot_name=bot_user.full_name,
            ),
            reply_markup=keyboards.agree_rules_keyboard(worker.id),
        )
    else:
        await welcome_new_user(message)
        return
    try:
        Worker.get(uniq_key=uniq_key)
    except Worker.DoesNotExist:
        await message.answer(texts.invalid_code)


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "agreerules", state="*")
async def agree_rules(query: types.CallbackQuery):
    worker_id = int(query.data.split("_")[1])
    try:
        worker = Worker.get(id=worker_id)

        await query.message.delete()
        await create_user(worker, query.message)
    except Worker.DoesNotExist:
        await query.message.edit_text(texts.invalid_code)


@dp.message_handler(state=Registration.code, is_user=False)
async def user_registration_code(message: types.Message, state: FSMContext):
    try:
        worker = Worker.get(uniq_key=message.text)
        bot_user = await dp.bot.get_me()
        await message.answer(
            texts.rules.format(
                name=message.chat.full_name,
                bot_name=bot_user.full_name,
            ),
            reply_markup=keyboards.agree_rules_keyboard(worker.id),
        )
        await state.finish()
    except Worker.DoesNotExist:
        await message.answer(texts.invalid_code)


@dp.message_handler(is_user=False, state="*")  # new user
async def welcome_new_user(message: types.Message):
    await message.answer(texts.new_user)
    await Registration.code.set()
