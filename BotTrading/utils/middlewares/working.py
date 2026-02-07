from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from customutils import load_config
from data.texts import dont_working_text, dont_working_alert


class WorkingMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, _):
        if not load_config().trading_work:
            await message.reply(dont_working_text)
            raise CancelHandler()

    async def on_process_callback_query(self, query: types.CallbackQuery, _):
        if not load_config().trading_work:
            await query.answer(dont_working_alert, show_alert=True)
            raise CancelHandler()
