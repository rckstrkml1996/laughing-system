import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data import config


"""
Обьявление приложения fastapi
Обьявление всех компонентов бота из конфига
"""
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Origin", "X-Requested-With",
                   "Content-Type", "Accept", "Authorization"],
)


bot = Bot(config.API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
