from aiogram import types
from aiogram.dispatcher import FSMContext


from loader import dp
from data.states import Code
from data.keyboards import main_keyboard, rules_keyboard
from data import payload
from models import TradingUser, Worker
from random import randint


@dp.message_handler(state="*", is_working=False)
async def on_dont_work_status(message: types.Message):
    await message.answer("Ожидайте завершения тех. работ, бот временно не работает!")


@dp.message_handler(commands="start")
async def welcome(message: types.Message):
    try:
        user = TradingUser.get(cid=message.chat.id)
        await message.answer(
            payload.my_profile_text.format(
                balance=user.balance, cid=user.cid, deals_count=randint(1900, 3000)
            ),
            reply_markup=main_keyboard,
        )
    except TradingUser.DoesNotExist:
        try:
            ref_id = message.text.split()[1]
            try:
                Worker.get(uniq_key=ref_id)
                await message.answer(
                    payload.welcome_text(message.from_user.full_name),
                    reply_markup=rules_keyboard(ref_id),
                )
            except Worker.DoesNotExist:
                await message.answer("Введите правильный 6 значный код.")
                await Code.main.set()

        except IndexError:
            await message.answer("Введите 6 значный код.")
            await Code.main.set()


@dp.message_handler(state=Code.main)
async def codecom(message: types.Message, state: FSMContext):
    try:
        Worker.get(uniq_key=message.text)
        await state.finish()
        await message.answer(
            payload.welcome_text(message.from_user.full_name),
            reply_markup=rules_keyboard(message.text),
        )
    except Worker.DoesNotExist:
        await message.answer("Неправильный код! Введите 6 значный код")


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "rulesagreed")
async def rules_agreed(query: types.CallbackQuery):
    ref_id = query.data.split("_")[1]
    try:
        worker = Worker.get(uniq_key=ref_id)
        await query.message.edit_text(
            payload.welcome_text(query.from_user.full_name, True)
        )
        user = TradingUser.create(
            owner=worker,
            cid=query.message.chat.id,
            username=query.from_user.username,
            fullname=query.from_user.full_name,
        )

        await query.message.answer(
            payload.my_profile_text.format(
                balance=user.balance, cid=user.cid, deals_count=randint(1900, 2500)
            ),
            reply_markup=main_keyboard,
        )
    except Worker.DoesNotExist:
        await query.message.delete()


# @dp.message_handler(content_types=["photo"])
# async def get_photo(message: types.Message):
#     file_id = message.photo[-1].file_id
#     print(file_id)  # этот идентификатор нужно где-то сохранить
#     await message.answer_photo(file_id)
