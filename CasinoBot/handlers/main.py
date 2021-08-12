from aiogram import types
from aiogram.types import ChatType
from aiogram.dispatcher.filters.builtin import Text
from aiogram.utils.exceptions import ChatNotFound
from aiogram.utils.deep_linking import get_start_link
from aiogram.dispatcher import FSMContext
from aiogram.utils.emoji import emojize
from loguru import logger

from data.config import LICENCE
from data.states import SelfCabine
import keyboards
from data import payload
from loader import dp
from customutils.models import User, UserHistory


async def self_cabine(chat_id: int):
    user = User.get(cid=chat_id)
    games = len(UserHistory.select().where(UserHistory.cid == chat_id,
                (UserHistory.editor == 2) | (UserHistory.editor == 3)))
    games_win = len(UserHistory.select().where(
        UserHistory.cid == chat_id, UserHistory.editor == 2))
    games_lose = len(UserHistory.select().where(
        UserHistory.cid == chat_id, UserHistory.editor == 3))

    # Сообщения для личного кабинета, не вынес в payload тк. нужен доступ к базе данных
    return emojize(f":pushpin: Личный кабинет \
		\n\n:dollar: Баланс: <b>{user.balance} RUB</b> \
		\n\n:high_brightness: Игр сыграно: <b>{games}</b>\
		\n:four_leaf_clover: Игр выиграно: <b>{games_win}</b>\
		\n:black_heart: Игр проиграно: <b>{games_lose}</b>\
		\n\n:bust_in_silhouette: Ваша реферальная ссылка :bust_in_silhouette: \
		\n{await get_start_link(user.id)} ")


@dp.message_handler(Text(startswith="личн", ignore_case=True), chat_type=ChatType.PRIVATE)
async def cabine(message: types.Message):
    await message.answer(await self_cabine(message.chat.id),
                         reply_markup=keyboards.selfcab_keyboard)  # main
    await SelfCabine.main.set()  # пустышка для перевода стейта


@dp.message_handler(chat_type=ChatType.PRIVATE, commands="start", state="*")
async def main_menu(message: types.Message, state: FSMContext):
    """
    Если юзер старый - личный кабинет
    Если нет в базе - политика конф.
    """
    chat_id = message.chat.id
    ref_id = 0
    try:
        ref_id = message.text.split()[1]
    except IndexError:
        logger.debug(f"{message.chat.first_name} #{chat_id} with out ref.")
    try:
        User.get(cid=chat_id)
        await message.answer(emojize("Вы попали в меню бота :clipboard:"),
                             reply_markup=keyboards.main_keyboard(message.chat.id))
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
    except User.DoesNotExist:
        await message.answer(payload.welcome_text(message.chat.first_name),
                             reply_markup=keyboards.welcome_keyboard(ref_id))


@dp.callback_query_handler(lambda cb: cb.data.split("_")[0] == "accept",
                           chat_type=ChatType.PRIVATE, state="*")
async def accept_user(call: types.CallbackQuery):
    """ Ответ на инлайн кнопку принять Политику """
    chat_id = call.message.chat.id
    try:
        User.get(cid=chat_id)
    except User.DoesNotExist:
        username = call.message.chat.username
        username = f"@{username}" if username else "Нет юзернейма"
        try:
            refer = User.get(id=call.data.split("_")[1])
            refer = refer.cid
        except User.DoesNotExist:
            refer = 0
        fullname = call.message.chat.full_name
        User.create(cid=chat_id, refer=refer, username=username,
                    fullname=fullname)  # ред на main
        if refer != 0:
            try:
                await dp.bot.send_message(refer, emojize(f":alien: Новый реферал \
					\n{call.message.chat.full_name} \
					\nid: <b>{chat_id}</b> - {username}"))
            except ChatNotFound:
                logger.warning(f"chat with refer {refer} does not exist")
    finally:
        await call.message.delete()
        await call.message.answer(await self_cabine(chat_id), reply_markup=keyboards.main_keyboard(call.message.chat.id))


@dp.message_handler(Text(startswith="инф", ignore_case=True), chat_type=ChatType.PRIVATE, state="*")
async def game_support(message: types.Message):
    await message.answer_photo(photo=LICENCE, caption=payload.info_text(), reply_markup=keyboards.main_keyboard(message.chat.id))
