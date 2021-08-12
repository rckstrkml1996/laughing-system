from random import randint

from aiogram import types
from aiogram.types import ChatType
from aiogram.utils.emoji import emojize
from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher import FSMContext
from loguru import logger

import keyboards
from data import payload
from data.states import Game
from loader import dp
from customutils.models import User, UserHistory


@dp.message_handler(commands=["game", "games"], state="*", chat_type=ChatType.PRIVATE)
@dp.message_handler(Text(startswith="игр", ignore_case=True),
                    state="*", chat_type=ChatType.PRIVATE)
async def play_game(message: types.Message):
    """
    Начало игры, перевод на стартовый стейт
    """
    try:
        user = User.get(cid=message.chat.id)
        await message.answer("Выберите интересующую Вас игру", reply_markup=keyboards.games_keyboard)
        await Game.chose_game.set()
    except User.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(Text(startswith="кост", ignore_case=True),
                    chat_type=ChatType.PRIVATE, state=Game.chose_game)
async def dice_game(message: types.Message):
    """
    Начало dice, перевод на стейт
    """
    try:
        user = User.get(cid=message.chat.id)
        await message.answer(payload.game_any, reply_markup=keyboards.play_keyboard)
        await Game.dice_anymes.set()
    except User.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(chat_type=ChatType.PRIVATE, state=Game.dice_anymes)
async def dice_any(message: types.Message):
    """
    Любое сообщение для старта
    """
    try:
        user = User.get(cid=message.chat.id)
        await message.answer(payload.game_amount(user.balance), reply_markup=keyboards.play_keyboard)
        await Game.dice_stake.set()
    except User.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(lambda mes: not mes.text.isdigit() or mes.text == '0',
                    chat_type=ChatType.PRIVATE, state=Game.dice_stake)
async def dice_stake_invalid(message: types.Message):
    await message.reply("Некорректное значение ставки!", reply_markup=keyboards.play_keyboard)


@dp.message_handler(chat_type=ChatType.PRIVATE, state=Game.dice_stake)
async def dice_stake(message: types.Message, state: FSMContext):
    """
    Принимаем ставку
    """
    try:
        user = User.get(cid=message.chat.id)
        amount = int(message.text)
        if user.balance >= int(message.text):
            user_dice = await message.answer_dice()
            bot_dice = await message.answer_dice()
            if user_dice.dice.value > bot_dice.dice.value:
                await message.answer(emojize(f":heart: Вы победили! \
					\nВаше число - {user_dice.dice.value}, число бота - {bot_dice.dice.value}"))
                user.balance += amount
                user.save()
                UserHistory.create(
                    cid=message.chat.id, amount=amount, balance=user.balance, editor=2)
            elif bot_dice.dice.value > user_dice.dice.value:
                await message.answer(emojize(f":broken_heart: Вы проиграли! \
					\nВаше число - {user_dice.dice.value}, число бота - {bot_dice.dice.value}"))
                user.balance -= amount
                user.save()
                UserHistory.create(
                    cid=message.chat.id, amount=amount, balance=user.balance, editor=3)
            else:
                await message.answer(emojize(f":white_heart: Ничья! \
					\nВаше число - {user_dice.dice.value}, число бота - {bot_dice.dice.value}"))
            await dice_any(message)
        else:
            await message.answer("Недостачно средств для ставки!", reply_markup=keyboards.play_keyboard)
    except User.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(Text(startswith="чис", ignore_case=True),
                    chat_type=ChatType.PRIVATE, state=Game.chose_game)
async def casino_game(message: types.Message):
    """
    Начало casino, перевод на стейт
    """
    try:
        user = User.get(cid=message.chat.id)
        await message.answer(payload.game_any, reply_markup=keyboards.play_keyboard)
        await Game.casino_anymes.set()
    except User.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(chat_type=ChatType.PRIVATE, state=Game.casino_anymes)
async def casino_any(message: types.Message):
    """
    Любое сообщение для старта
    """
    try:
        user = User.get(cid=message.chat.id)
        await message.answer(payload.game_amount(user.balance), reply_markup=keyboards.play_keyboard)
        await Game.casino_stake.set()
    except User.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(lambda mes: not mes.text.isdigit() or mes.text == '0',
                    chat_type=ChatType.PRIVATE, state=Game.casino_stake)
async def casino_stake_invalid(message: types.Message):
    await message.reply("Некорректное значение ставки!", reply_markup=keyboards.play_keyboard)


@dp.message_handler(chat_type=ChatType.PRIVATE, state=Game.casino_stake)
async def casino_stake(message: types.Message, state: FSMContext):
    """
    Принимаем ставку
    """
    try:
        user = User.get(cid=message.chat.id)
        if user.balance >= int(message.text):
            async with state.proxy() as data:
                data['stake'] = int(message.text)
            await message.answer(payload.game_bet, reply_markup=keyboards.bet_keyboard)
            await Game.casino_bet.set()
        else:
            await message.answer("Недостачно средств для ставки!", reply_markup=keyboards.play_keyboard)
    except User.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(regexp="(>|=|<)\s*50", chat_type=ChatType.PRIVATE, state=Game.casino_bet)
async def casino_bet(message: types.Message, state: FSMContext, regexp):
    """
    В зависимости от статуса игрока - придумываем число
    """
    try:
        user = User.get(cid=message.chat.id)
        if user.balance > 200000:
            user.premium = False
        if user.premium:
            number = int(regexp.group(0)[1:])
            if regexp.group(0)[0] == ">":
                number = randint(51, 99)
            elif regexp.group(0)[0] == "<":
                number = randint(1, 49)

            moll = 10 if number == 50 else 2
            async with state.proxy() as data:
                amount = data['stake'] * moll - data['stake']
                user.balance += amount
                user.save()
                UserHistory.create(
                    cid=message.chat.id, amount=amount, balance=user.balance, editor=2)

            await message.answer(f"Победа! Выпало число {number}")
        else:
            number = regexp.group(0)[0]
            if regexp.group(0)[0] == ">":
                number = randint(1, 49)
            elif regexp.group(0)[0] == "<":
                number = randint(51, 99)
            else:
                number = randint(1, 99)
                if number == 50:
                    number = 69  # да я еблан

            async with state.proxy() as data:
                user.balance -= data['stake']
                user.save()
                UserHistory.create(cid=message.chat.id, editor=3,
                                   amount=data['stake'], balance=user.balance)
            await message.answer(emojize(f"Вы проиграли :confused: Выпало число {number}"))

        await casino_any(message)
    except User.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(chat_type=ChatType.PRIVATE, state=Game.casino_bet)
async def casino_bet_invalid(message: types.Message):
    await message.answer("Вы ввели некоректное значение ставки \
		\n\n< 50 - x2\n= 50 - x10\n> 50 - x2")
