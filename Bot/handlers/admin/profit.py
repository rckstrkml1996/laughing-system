from aiogram.types import Message

from loader import dp, payments_checker
from data.texts import make_profit_text
from data.states import MakeProfit


@dp.message_handler(
    commands=["prft", "profit", "make_profit"],
    admins_chat=True,
    is_admin=True,
    state="*",
)
async def make_profit_command(message: Message):
    await message.answer(make_profit_text)
    await MakeProfit.main.set()


@dp.message_handler(state=MakeProfit.main, admins_chat=True, is_admin=True)
async def make_profit_main(message: Message):
    data = message.text.split("\n")  # id, amount, share, service

    if len(data) >= 4:
        service_names = list(
            filter(
                lambda x: x.lower() in data[3].lower(), payments_checker.SERVICE_NAMES
            )
        )
        if (
            data[0].isdigit()
            and data[1].isdigit()
            and data[2].isdigit()
            and service_names
        ):
            telegram_id = int(data[0])  # 321321302
            amount = int(data[1])  # 1000
            moll = int(data[2])  # 80
            service = data[3]  # just wrap

            print(
                telegram_id,
                amount,
                moll,
                service
            )

            return

    await message.answer("Неправильно заполнил данные")
