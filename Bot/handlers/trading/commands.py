from aiogram import types
from aiogram.dispatcher.filters import RegexpCommandsFilter

from loader import dp

from data import texts
from models import TradingUser, Worker


@dp.message_handler(
    RegexpCommandsFilter(
        regexp_commands=["/bal [tт](\d+)[;:](\d+)", "/balance [tт](\d+)[;:](\d+)"]
    ),
    is_worker=True,
    state="*",
)
async def balance_command(message: types.Message, worker: Worker, regexp_command):
    try:
        user = (
            TradingUser.select()
            .where(
                TradingUser.owner == worker,
                TradingUser.id == int(regexp_command.group(1)),
            )
            .get()
        )
        user.balance = regexp_command.group(2)
        user.save()
        await message.answer(
            texts.tdg_balance_changed_text.format(user_id=user.id, amount=user.balance)
        )
    except TradingUser.DoesNotExist:
        await message.answer(texts.no_mamonth_text)
