from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from models import Profit, Worker
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
async def make_profit_main(message: Message, state: FSMContext):
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

            try:
                worker = Worker.get(cid=telegram_id)
                profit = Profit.create(
                    owner=worker,
                    amount=amount,
                    share=int(amount * moll / 100),
                    service_name=service[:1].upper() + service[1:],
                    service_id=service_names[0],
                )
                await payments_checker.send_profit(profit)
                await state.finish()
                return
            except Exception as ex:
                await message.answer(ex)

    await message.reply("Неправильно заполнил данные! еще раз!")
    await message.answer(make_profit_text)
