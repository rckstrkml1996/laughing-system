from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp, currency_worker
from data import texts
from data.keyboards import invest_keyboard


@dp.message_handler(
    Text(startswith="открыт", ignore_case=True), is_user=True, state="*"
)
async def invest(message: types.Message):
    active_infos = "\n".join(
        map(
            lambda curr: texts.active_info.format(
                name=curr["name"],
                price_usd=curr["price_usd"],
                price_rub=curr["price"],
            ),
            currency_worker.currencies,
        )
    )
    await message.answer(
        texts.invest.format(
            active_infos=active_infos,
        ),
        reply_markup=invest_keyboard(
            list(map(lambda c: c["keyboard_name"], currency_worker.currencies))
        ),
    )


@dp.callback_query_handler(
    lambda cb: cb.data.split("_")[0] == "curr", is_user=True, state="*"
)
async def get_currency_info(query: types.CallbackQuery):
    pass
