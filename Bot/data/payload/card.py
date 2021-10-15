from aiogram.utils.emoji import emojize


going_card_text = emojize(
    ":credit_card: Введите <b>новую карту</b> для прямых переводов:"
)


outgoing_card_text = emojize(
    ":ear_of_rice: <i>Новая карта:</i> <b>{card}</b>\nДобавленна!"
)

oldnew_card_text = emojize(
    ":briefs: <i>Старая карта:</i> {old_card}\n"
    ":star: <i>Новая карта:</i> <b>{new_card}</b>\nДобавленна!"
)
