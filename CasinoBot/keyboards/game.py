from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.emoji import emojize


games_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
casino_button = KeyboardButton(emojize("Числа"))
dice_button = KeyboardButton(emojize("Кости"))
cancel_button = KeyboardButton(emojize("Назад"))
games_keyboard.add(casino_button, dice_button)
games_keyboard.add(cancel_button)

# game keyboard
play_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
end_game_button = KeyboardButton("Закончить игру")
play_keyboard.add(end_game_button)

bet_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
low_button = KeyboardButton("<50")
equal_button = KeyboardButton("=50")
high_button = KeyboardButton(">50")
cancel_button = KeyboardButton("Закончить игру")
bet_keyboard.add(low_button, equal_button, high_button, cancel_button)
