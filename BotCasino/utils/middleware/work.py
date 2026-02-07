from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from customutils import load_config
from models import CasinoUser
from data.texts import dont_working_text, dont_working_alert


class WorkingMiddleware(BaseMiddleware):
    def __init__(self):
        super(WorkingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, _):
        if not load_config().casino_work:
            await message.reply(dont_working_text)
            raise CancelHandler()

        try:
            worker = CasinoUser.get(cid=message.chat.id)
            if worker.stopped:
                await message.reply(dont_working_text)
                raise CancelHandler()
        except CasinoUser.DoesNotExist:
            pass

    async def on_process_callback_query(self, query: types.CallbackQuery, _):
        if not load_config().casino_work:
            await query.answer(dont_working_alert, show_alert=True)
            raise CancelHandler()

        try:
            worker = CasinoUser.get(cid=query.from_user.id)
            if worker.stopped:
                await query.answer(dont_working_text)
                raise CancelHandler()
        except CasinoUser.DoesNotExist:
            pass
