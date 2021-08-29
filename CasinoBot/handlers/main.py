import re

from aiogram import types
from aiogram.types import ChatType
from aiogram.dispatcher.filters.builtin import Text
from aiogram.utils.deep_linking import get_start_link
from aiogram.dispatcher import FSMContext
from aiogram.utils.emoji import emojize
from loguru import logger

from config import LICENCE
from data.states import SelfCabine, Register
import keyboards
from data import payload
from loader import dp
from customutils.models import Worker, CasinoUser, CasinoUserHistory


@dp.message_handler(state="*", is_working=False)
async def on_dont_work_status(message: types.Message):
    await message.answer("Ожидайте завершения тех. работ, бот временно не работает!")


async def self_cabine(chat_id: int):
    user = CasinoUser.get(cid=chat_id)
    games = user.history.where(
        (CasinoUserHistory.editor == 2) | (CasinoUserHistory.editor == 3)
    ).count()
    games_win = user.history.where(CasinoUserHistory.editor == 2).count()
    games_lose = user.history.where(CasinoUserHistory.editor == 3).count()

    # Сообщения для личного кабинета, не вынес в payload тк. нужен доступ к базе данных
    return emojize(
        f":pushpin: Личный кабинет \
		\n\n:dollar: Баланс: <b>{user.balance} RUB</b> \
		\n\n:high_brightness: Игр сыграно: <b>{games}</b>\
		\n:four_leaf_clover: Игр выиграно: <b>{games_win}</b>\
		\n:black_heart: Игр проиграно: <b>{games_lose}</b>\
		\n\n:bust_in_silhouette: Ваша реферальная ссылка :bust_in_silhouette: \
		\n{await get_start_link(user.id)} "
    )


@dp.message_handler(Text(startswith="личн", ignore_case=True))
async def cabine(message: types.Message):
    await message.answer(
        await self_cabine(message.chat.id)
    )  # main
    await SelfCabine.main.set()  # пустышка для перевода стейта


async def ref_code(message: types.Message):
    await message.answer("Введи код")
    await Register.ref_code.set()


@dp.message_handler(state=Register.ref_code)
async def register(message: types.Message, state: FSMContext):
    mtch = re.search(r"\d{6}", message.text)
    if mtch:
        try:
            Worker.get(uniq_key=mtch.group(0))
            await message.answer(
                payload.welcome_text(message.chat.first_name),
                reply_markup=keyboards.welcome_keyboard(mtch.group(0)),
            )
            await state.finish()
        except Worker.DoesNotExist:
            await message.answer("Введи правильный код")
    else:
        await message.answer("Введи правильный код")


@dp.message_handler(commands="start", state="*")
async def main_menu(message: types.Message, state: FSMContext):
    """
    Если юзер старый - личный кабинет
    Если нет в базе - политика конф.
    """
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    chat_id = message.chat.id
    try:
        CasinoUser.get(cid=chat_id)
        await message.answer(
            emojize("Вы попали в меню бота :clipboard:"),
            reply_markup=keyboards.main_keyboard(),
        )
    except CasinoUser.DoesNotExist:
        try:
            ref_id = message.text.split()[1]
            await message.answer(
                payload.welcome_text(message.chat.first_name),
                reply_markup=keyboards.welcome_keyboard(ref_id),
            )
        except IndexError:
            await ref_code(message)


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "accept", state="*")
async def accept_user(query: types.CallbackQuery):
    # Ответ на инлайн кнопку принять Политику
    chat_id = query.message.chat.id
    refer = query.data.split("_")[1]
    if refer == "0":
        await ref_code(message)
        return

    try:
        CasinoUser.get(cid=chat_id)
    except CasinoUser.DoesNotExist:
        try:
            worker = Worker.get(uniq_key=refer)
            username = query.message.chat.username
            fullname = query.message.chat.full_name
            CasinoUser.create(
                owner=worker, cid=chat_id, username=username, fullname=fullname
            )
        except Worker.DoesNotExist:  # редко
            await ref_code(query.message)
            return
    finally:
        await query.message.answer(
            await self_cabine(chat_id), reply_markup=keyboards.main_keyboard()
        )
        await query.message.delete()


@dp.message_handler(Text(startswith="инф", ignore_case=True), state="*")
async def game_support(message: types.Message):
    # await message.answer_photo(photo=LICENCE, caption=payload.info_text(), reply_markup=keyboards.main_keyboard())
    await message.answer(payload.info_text(), reply_markup=keyboards.main_keyboard())


@dp.message_handler(regexp="назад", state="*")
async def cancel(message: types.Message, state: FSMContext):
    await main_menu(message, state)
