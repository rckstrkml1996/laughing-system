import re

from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters import BoundFilter
from loguru import logger

from customutils.models import Worker

from config import config  # ADMINS_ID


class SendSummaryFilter(BoundFilter):
    key = "send_summary"  # working for query and message handlers

    def __init__(self, send_summary):
        self.send_summary = send_summary

    def get_target(self, obj):
        if isinstance(obj, CallbackQuery):
            return obj.message.chat  # if query
        return obj.chat  # if message

    async def check(self, obj):
        chat = self.get_target(obj)
        if chat.type == "private":
            try:
                return Worker.get(cid=chat.id).send_summary == self.send_summary
            except Worker.DoesNotExist:
                pass
        return False


class AdminsChatFilter(BoundFilter):
    key = "admins_chat"
    required = True
    default = False

    def get_target(self, obj):
        if isinstance(obj, CallbackQuery):
            return obj.message.chat  # if query
        return obj.chat  # if message

    def __init__(self, admins_chat):
        self.admins_chat = admins_chat

    async def check(self, obj):
        if self.admins_chat == "*":
            return True

        chat = self.get_target(obj)
        if chat.id == config("admins_chat"):
            return self.admins_chat
        return not self.admins_chat


class WorkersChatFilter(BoundFilter):
    key = "workers_chat"
    required = True
    default = False

    def get_target(self, obj):
        if isinstance(obj, CallbackQuery):
            return obj.message.chat  # if query
        return obj.chat  # if message

    def __init__(self, workers_chat):
        self.workers_chat = workers_chat

    async def check(self, obj):
        if self.workers_chat == "*":
            return True

        chat = self.get_target(obj)
        if chat.id == config("workers_chat"):
            return self.workers_chat
        return not self.workers_chat


class FullRegexpCommandsFilter(BoundFilter):
    key = "fullregexp_commands"

    def __init__(self, fullregexp_commands):
        self.regexp_commands = [
            re.compile(command, flags=re.IGNORECASE | re.MULTILINE)
            for command in fullregexp_commands
        ]

    async def check(self, message: Message):
        if not message.is_command():
            return False

        for command in self.regexp_commands:
            match = command.match(message.text[1:])
            if match:
                return {"full_regexp": match}

        return False
