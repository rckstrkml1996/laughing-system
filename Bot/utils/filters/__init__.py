from aiogram import Dispatcher

from .main import IsWorkerFilter, SendSummaryFilter, AdminsChatFilter, WorkersChatFilter


def setup(dp: Dispatcher):
    event_handlers = [
        dp.message_handlers,
        dp.edited_message_handlers,
        dp.callback_query_handlers,
    ]

    dp.filters_factory.bind(
        IsWorkerFilter, event_handlers=event_handlers
    )
    dp.filters_factory.bind(
        SendSummaryFilter, event_handlers=event_handlers
    )
    dp.filters_factory.bind(
        AdminsChatFilter, event_handlers=event_handlers
    )
    dp.filters_factory.bind(
        WorkersChatFilter, event_handlers=event_handlers
    )
