from asyncio import sleep
from random import randint

from aiogram import types
from aiogram.utils.emoji import emojize
from aiogram.dispatcher.filters.builtin import Text
from aiogram.dispatcher import FSMContext
from loguru import logger

from data import keyboards, texts
from data.states import Game
from loader import dp
from models import CasinoUser, CasinoUserHistory


@dp.message_handler(regexp="закончить игру", state="*")
async def cancel_game(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()

    await play_game(message)


@dp.message_handler(commands=["game", "games"], state="*")
@dp.message_handler(Text(startswith="игр", ignore_case=True), state="*")
async def play_game(message: types.Message):
    """
    Начало игры, перевод на стартовый стейт
    """
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(  ####
            "Выберите интересующую Вас игру", reply_markup=keyboards.games_keyboard
        )
        await Game.chose_game.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(Text(startswith="кост", ignore_case=True), state=Game.chose_game)
async def dice_game(message: types.Message):
    """
    Начало dice, перевод на стейт
    """
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(texts.game_any, reply_markup=keyboards.play_keyboard)
        await Game.dice_anymes.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(state=Game.dice_anymes)
async def dice_any(message: types.Message):
    """
    Любое сообщение для старта
    """
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(
            texts.game_amount.format(amount=user.balance),
            reply_markup=keyboards.play_keyboard,
        )
        await Game.dice_stake.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(
    lambda mes: not mes.text.isdigit() or mes.text == "0", state=Game.dice_stake
)
async def dice_stake_invalid(message: types.Message):
    await message.reply(
        "Некорректное значение ставки!", reply_markup=keyboards.play_keyboard  #####
    )
    logger.debug(f"{message.chat.id} - wrong bet value")


@dp.message_handler(state=Game.dice_stake)
async def dice_stake(message: types.Message, state: FSMContext):
    """
    Принимаем ставку
    """
    try:
        user = CasinoUser.get(cid=message.chat.id)
        amount = int(message.text)
        if user.balance >= int(message.text):
            user_dice = await message.answer_dice()
            bot_dice = await message.answer_dice()
            if user_dice.dice.value > bot_dice.dice.value:
                await message.answer(
                    emojize(
                        f":green_heart: Вы победили! \
					\nВаше число - {user_dice.dice.value}, число бота - {bot_dice.dice.value}"  ###
                    )
                )
                user.balance += amount
                user.save()
                CasinoUserHistory.create(
                    owner=user, amount=amount, balance=user.balance, editor=2
                )
                logger.debug(f"{message.chat.id} - won")
            elif bot_dice.dice.value > user_dice.dice.value:
                await message.answer(
                    emojize(  ####
                        f":broken_heart: Вы проиграли! \
					\nВаше число - {user_dice.dice.value}, число бота - {bot_dice.dice.value}"
                    )
                )
                user.balance -= amount
                user.save()
                CasinoUserHistory.create(
                    owner=user, amount=amount, balance=user.balance, editor=3
                )
                logger.debug(f"{message.chat.id} - lose")
            else:
                await message.answer(
                    emojize(
                        f":white_heart: Ничья! \
					\nВаше число - {user_dice.dice.value}, число бота - {bot_dice.dice.value}"
                    )
                )
                logger.debug(f"{message.chat.id} - draw")
            await dice_any(message)
        else:
            await message.answer(
                "Недостачно средств для ставки!", reply_markup=keyboards.play_keyboard
            )
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id} - not enough money")


@dp.message_handler(Text(startswith="числ", ignore_case=True), state=Game.chose_game)
async def casino_game(message: types.Message):
    """
    Начало casino, перевод на стейт
    """
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(texts.game_any, reply_markup=keyboards.play_keyboard)
        await Game.casino_anymes.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(state=Game.casino_anymes)
async def casino_any(message: types.Message):
    """
    Любое сообщение для старта
    """
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(
            texts.game_amount.format(amount=user.balance),
            reply_markup=keyboards.play_keyboard,
        )
        await Game.casino_stake.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(
    lambda mes: not mes.text.isdigit() or mes.text == "0", state=Game.casino_stake
)
async def casino_stake_invalid(message: types.Message):
    await message.reply(
        "Некорректное значение ставки!", reply_markup=keyboards.play_keyboard
    )
    logger.debug(f"{message.chat.id} - wrong bet value")


@dp.message_handler(state=Game.casino_stake)
async def casino_stake(message: types.Message, state: FSMContext):
    """
    Принимаем ставку
    """
    try:
        user = CasinoUser.get(cid=message.chat.id)
        if user.balance >= int(message.text):
            async with state.proxy() as data:
                data["stake"] = int(message.text)
            await message.answer(texts.game_bet, reply_markup=keyboards.bet_keyboard)
            await Game.casino_bet.set()
        else:
            await message.answer(
                "Недостачно средств для ставки!",
                reply_markup=keyboards.play_keyboard,  ####
            )
            logger.debug(f"{message.chat.id} - not enough money")
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(regexp="(>|=|<)\s*50", state=Game.casino_bet)
async def casino_bet(message: types.Message, state: FSMContext, regexp):
    """
    В зависимости от статуса игрока - придумываем число
    """
    try:
        user = CasinoUser.get(cid=message.chat.id)
        if user.balance > 200000:
            user.fort_chance = 30

        rand = randint(0, 99)

        win = False
        bet = regexp.group(0)

        if bet[0] == "=":
            c = randint(0, 4950)
            if user.fort_chance == 100:
                win = True
            elif c < user.fort_chance:
                win = True
        else:
            if rand < user.fort_chance:
                win = True

        if win:
            if bet[0] == ">":
                number = randint(51, 99)
            elif bet[0] == "<":
                number = randint(1, 49)
            elif bet[0] == "=":
                number = 50

            moll = 10 if number == 50 else 2
            async with state.proxy() as data:
                amount = data["stake"] * moll - data["stake"]
                user.balance += amount
                user.save()
                CasinoUserHistory.create(
                    owner=user, amount=amount, balance=user.balance, editor=2
                )

            await message.answer(f"Победа! Выпало число {number}")
        else:
            if bet[0] == ">":
                number = randint(1, 49)
            elif bet[0] == "<":
                number = randint(51, 99)
            elif bet[0] == "=":
                onetwo = randint(1, 2)
                if onetwo == 1:
                    number = randint(1, 49)
                else:
                    number = randint(51, 99)

            async with state.proxy() as data:
                amount = data["stake"]
                user.balance -= data["stake"]
                user.save()
                CasinoUserHistory.create(
                    owner=user, amount=amount, balance=user.balance, editor=3
                )

            await message.answer(
                emojize(f"Вы проиграли :confused: Выпало число {number}")
            )

        await casino_any(message)
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(state=Game.casino_bet)
async def casino_bet_invalid(message: types.Message):
    await message.answer(
        "Вы ввели некоректное значение ставки \
		\n\n&lt; 50 - x2\n= 50 - x10\n&gt; 50 - x2"
    )


@dp.message_handler(Text(startswith="граф", ignore_case=True), state=Game.chose_game)
async def graph_game(message: types.Message):
    """
    Начало dice, перевод на стейт
    """
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(texts.game_any, reply_markup=keyboards.play_keyboard)
        await Game.graph_anymes.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(state=Game.graph_anymes)
async def graph_any(message: types.Message):
    """
    Любое сообщение для старта
    """
    try:
        user = CasinoUser.get(cid=message.chat.id)
        await message.answer(
            texts.game_amount.format(amount=user.balance),
            reply_markup=keyboards.play_keyboard,
        )
        await Game.graph_stake.set()
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id} - does not exist")


@dp.message_handler(
    lambda mes: not mes.text.isdigit() or mes.text == "0", state=Game.graph_stake
)
async def graph_stake_invalid(message: types.Message):
    await message.reply(
        "Некорректное значение ставки!", reply_markup=keyboards.play_keyboard
    )
    logger.debug(f"{message.chat.id} - wrong bet value")


@dp.message_handler(state=Game.graph_stake)
async def graph_stake(message: types.Message, state: FSMContext):
    # Принимаем ставку
    amount = int(message.text)
    try:
        user = CasinoUser.get(cid=message.chat.id)
        if user.balance > 200000:
            user.fort_chance = 40

        if user.balance >= amount:
            user.balance -= amount
            user.save()
            await message.answer(
                emojize(
                    ":ok_hand: <b>Ставка засчитана</b>, следите за коэффициентом и заберите деньги вовремя!"
                ),
                reply_markup=keyboards.stop_graph_keyboard,
            )
            working = True
            value = 0.1
            msg = await message.answer(texts.graph.format(value=value))
            await Game.graph_set_stop.set()
            while working:
                await sleep(0.4)
                current_state = await state.get_state()
                working = current_state == "Game:graph_set_stop"
                # print(current_state)
                # print(working)

                value += 0.07
                value *= 1.03
                try:
                    await msg.edit_text(texts.graph.format(value=value))
                except Exception as ex:
                    logger.error(ex)

                if value > 30:
                    if user.fort_chance == 100:
                        amount *= value
                        user.balance += amount
                        user.save()
                        CasinoUserHistory.create(
                            owner=user, amount=amount, balance=user.balance, editor=2
                        )
                        await message.answer(texts.graph_win.format(amount=amount))
                        await graph_any(message)
                    elif user.fort_chance >= randint(1, 99):  # if 1 of 100
                        amount *= value
                        user.balance += amount
                        user.save()
                        CasinoUserHistory.create(
                            owner=user, amount=amount, balance=user.balance, editor=2
                        )
                        await message.answer(texts.graph_win.format(amount=amount))
                        await graph_any(message)
                    else:
                        amount *= value
                        if user.balance < amount:
                            amount = user.balance
                        user.balance -= amount
                        user.save()
                        CasinoUserHistory.create(
                            owner=user, amount=amount, balance=user.balance, editor=3
                        )  # как проигрыш
                        await message.answer(texts.graph_lose.format(amount=amount))
                        await graph_any(message)
                    return

            current_state = await state.get_state()
            if current_state == "Game:graph_stop":
                await msg.edit_text("График остановлен.")
                if user.fort_chance == 100:
                    amount *= value
                    user.balance += amount
                    user.save()
                    CasinoUserHistory.create(
                        owner=user, amount=amount, balance=user.balance, editor=2
                    )
                    await message.answer(texts.graph_win.format(amount=amount))
                    await graph_any(message)
                elif user.fort_chance >= randint(1, 99):  # if 1 of 100
                    amount *= value  # shit code
                    user.balance += amount
                    user.save()
                    CasinoUserHistory.create(
                        owner=user, amount=amount, balance=user.balance, editor=2
                    )
                    await message.answer(texts.graph_win.format(amount=amount))
                    await graph_any(message)
                else:
                    amount *= value
                    if user.balance < amount:
                        amount = user.balance
                    user.balance -= amount
                    user.save()
                    CasinoUserHistory.create(
                        owner=user, amount=amount, balance=user.balance, editor=3
                    )  # как проигрыш
                    await message.answer(texts.graph_lose.format(amount=amount))
                    await graph_any(message)
            else:
                CasinoUserHistory.create(
                    owner=user, amount=amount, balance=user.balance, editor=3
                )  # как проигрыш
                await message.answer(
                    f"Вы не выбрали значения по графику, <b>{amount} RUB</b> списанны."
                )
        else:
            await message.answer(
                "Недостачно средств для ставки!", reply_markup=keyboards.play_keyboard
            )
    except CasinoUser.DoesNotExist:
        logger.debug(f"{message.chat.id} - not enough money")


@dp.message_handler(regexp="остан", state=Game.graph_set_stop)
async def graph_stop():
    await Game.graph_stop.set()  # just set it stopped;
