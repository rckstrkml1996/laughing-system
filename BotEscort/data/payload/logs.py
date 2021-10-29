from aiogram.utils.emoji import emojize


newref_ref_text = emojize(
    ":kiss: (/e{m_id}) - <a href='tg://user?id={chat_id}'>{name}</a> перешёл по твоей <i>реферальной ссылке</i>."
)

newref_code_text = emojize(
    ":kiss: (/e{m_id}) - <a href='tg://user?id={chat_id}'>{name}</a> ввёл твой <i>код доступа</i>."
)
