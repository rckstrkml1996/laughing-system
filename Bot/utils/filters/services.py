from typing import Iterable, Optional

from aiogram.dispatcher.filters import RegexpCommandsFilter


class ServiceCommandsFilter(RegexpCommandsFilter):
    CASINO_FIRST_LETTERS = ["c", "C", "с", "С"]
    ESCORT_FIRST_LETTERS = ["e", "E", "е", "Е"]
    TRADING_FIRST_LETTERS = ["t", "T", "т", "Т"]

    SERVICE_FIRST_LETTERS = [
        *CASINO_FIRST_LETTERS,
        *ESCORT_FIRST_LETTERS,
        *TRADING_FIRST_LETTERS,
    ]

    def __init__(
        self,
        command_names: Iterable[str],
        services: Iterable[str],
        with_id: Optional[bool] = None,
        with_text: Optional[bool] = None,
    ):
        cm_services = "(" + "\d+|".join(services) + "\d+)"
        if with_id:
            cm_services += "[\;\:](\d+)"
        elif with_text:
            cm_services += "[\;\:](.+)"

        super().__init__(
            regexp_commands=list(map(lambda cn: f"{cn} {cm_services}", command_names))
        )
