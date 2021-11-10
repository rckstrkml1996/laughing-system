from aiogram.types.message import Message
from models.models import TradingUser
from aiogram.types import Message

from loader import dp

from models import TradingUser
from .profile import profile


@dp.message_handler(is_user=True, state="*")
async def any_message(message: Message, user: TradingUser):
    await profile(message, user)
