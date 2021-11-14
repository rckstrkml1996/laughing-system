from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import config, dp
from customutils import save_config
from data.texts import going_card_text, outgoing_card_text, oldnew_card_text
from data.states import Card


@dp.message_handler(commands="card", is_admin=True, admins_chat=True, state="*")
async def card(message: types.Message):
    await message.answer(going_card_text)
    await Card.main.set()


@dp.message_handler(state=Card.main, is_admin=True, admins_chat=True)
async def new_card(message: types.Message, state: FSMContext):
    try:
        old_card = config.qiwi_card
        config.qiwi_card = message.text
        save_config(config)
        if old_card:
            await message.answer(
                oldnew_card_text.format(old_card=old_card, new_card=message.text)
            )
        else:
            await message.answer(outgoing_card_text.format(card=message.text))
    except Exception as ex:
        await message.answer(str(ex))
    await state.finish()
