from aiogram import types
from customutils.models import Worker, Profit
from customutils.models import CasinoUser, TradingUser, EscortUser

from loader import dp, db_commands
from data.payload import statistic_text


@dp.message_handler(commands=["stat", "statistic"], admins_chat=True, is_admin=True)
async def statistic_command(message: types.Message):
    profits_count = Profit.select().count()
    amount = db_commands.all_profits_sum()
    share = db_commands.all_share_sum()

    workers_today = db_commands.workers_today()

    try:
        middle_profits = int(amount / profits_count)
    except ZeroDivisionError:
        middle_profits = 0

    await message.answer(
        statistic_text.format(
            workers_count=Worker.select().where(Worker.status == 2).count(),
            bot_users_count=Worker.select().count(),
            casino_count=CasinoUser.select().count(),
            escort_count=EscortUser.select().count(),
            trading_count=TradingUser.select().count(),
            profits_count=profits_count,
            profits_amount=amount,
            profits_middle=middle_profits,
            profits_cash=amount - share,  # as int
            workers_count_today=0,
            bot_users_count_today=0,
            profits_count_today=0,
            profits_amount_today=0,
            profits_middle_today=0,
            profits_cash_today=0,
        )
    )
