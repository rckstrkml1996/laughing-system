from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from data.states import Add, Out, Bet, Registration
from .invest import *
from .profile import *
from .registration import *
from .reinforcement import *


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        add, Text(startswith="пополнить", ignore_case=True), state="*", is_user=True
    )
    dispatcher.register_message_handler(
        out, Text(startswith="вывести", ignore_case=True), state="*", is_user=True
    )
    dispatcher.register_message_handler(
        invest_handler,
        Text(startswith="открыть", ignore_case=True),
        state="*",
        is_user=True,
    )

    dispatcher.register_callback_query_handler(
        add_pay_card, text="paycard", state="*", is_user=True
    )

    dispatcher.register_message_handler(out_number, state=Out.main, is_user=True)

    dispatcher.register_message_handler(
        invalid_add_amount,
        lambda msg: not msg.text.isdigit(),
        state=Add.main,
        is_user=True,
    )
    dispatcher.register_message_handler(
        add_amount,
        state=Add.main,
        is_user=True,
    )
    dispatcher.register_callback_query_handler(
        add_check, lambda cb: cb.data.split("_")[0] == "check", state="*", is_user=True
    )

    dispatcher.register_callback_query_handler(
        get_currency_info,
        lambda cb: cb.data.split("_")[0] == "curr",
        state="*",
        is_user=True,
    )

    dispatcher.register_callback_query_handler(
        bet_handler, lambda cb: cb.data.split("_")[0] == "bet", state="*", is_user=True
    )
    dispatcher.register_message_handler(
        non_digit_bet_amount,
        lambda msg: not msg.text.isdigit(),
        state=Bet.amount,
        is_user=True,
    )
    dispatcher.register_message_handler(bet_amount, state=Bet.amount, is_user=True)
    dispatcher.register_callback_query_handler(
        time_selected,
        lambda cb: cb.data.split("_")[0] == "tchoice",
        state=Bet.time,
        is_user=True,
    )
    dispatcher.register_message_handler(portfile, state="*", is_user=True)

    dispatcher.register_callback_query_handler(
        agree_rules,
        lambda cb: cb.data.split("_")[0] == "agreerules",
        state="*",
        is_user=False,
    )
    dispatcher.register_message_handler(
        start_new_user, commands=["start"], state="*", is_user=False
    )
    dispatcher.register_message_handler(
        user_registration_code, state=Registration.code, is_user=False
    )
    dispatcher.register_message_handler(new_user, state="*", is_user=False)
