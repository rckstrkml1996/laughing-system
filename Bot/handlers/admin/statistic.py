from aiogram import types

from loader import dp
from utils import basefunctional
from models import Worker, Profit, CasinoUser, TradingUser, EscortUser
from data.payload import statistic_text


@dp.message_handler(commands=["stat", "statistic"], admins_chat=True, is_admin=True)
async def statistic_command(message: types.Message):
    profits_count = Profit.select().count()
    amount = basefunctional.all_profits_sum()
    share = basefunctional.all_share_sum()
    try:
        middle_profits = int(amount / profits_count)
    except ZeroDivisionError:
        middle_profits = 0

    bot_users_today = basefunctional.workers_today()
    bot_users_today_count = bot_users_today.count()

    profits_today = basefunctional.get_profits_day()
    profits_today_count = profits_today.count()
    profits_amount_today = basefunctional.get_profits_day_amount()
    profits_share_today = basefunctional.get_profits_day_share()
    try:
        middle_profits_share = int(profits_amount_today / profits_today_count)
    except ZeroDivisionError:
        middle_profits_share = 0

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
            workers_count_today=bot_users_today.where(Worker.status == 2).count(),
            bot_users_count_today=bot_users_today_count,
            profits_count_today=profits_today_count,
            profits_amount_today=profits_amount_today,
            profits_middle_today=middle_profits_share,
            profits_cash_today=profits_amount_today - profits_share_today,
        )
    )
