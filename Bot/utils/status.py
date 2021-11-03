from aiogram.utils.emoji import emojize


class StatusNames(list):
    VALUES = [
        "Без статуса",
        "Заблокирован",
        "Воркер",
        "Модер",
        "Сапорт ТП",
        "Кодер",
        "ТС",
        "Dungeon Master",
    ]

    def __init__(self):
        super().__init__(self.VALUES)

    @classmethod
    def get_value(cls, value_id: int = None):
        if value_id == 0:
            emoji = emojize(":black_square_button:")
        elif value_id == 1:
            emoji = emojize(":hankey:")
        elif value_id == 2:
            emoji = emojize(":man_technologist:")
        else:
            emoji = emojize(":sunglasses:")

        return f"{emoji} {cls.VALUES[value_id]}"
