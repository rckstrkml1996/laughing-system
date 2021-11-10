from aiogram import Dispatcher

from .users import IsUser


def setup_filters(dispatcher: Dispatcher):
    dispatcher.filters_factory.bind(IsUser, event_handlers=[
        dispatcher.message_handlers,
        dispatcher.callback_query_handlers
    ])
