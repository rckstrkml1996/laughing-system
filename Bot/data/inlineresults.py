from aiogram.types import InlineQueryResultArticle, InputTextMessageContent


def tagbot_article(art_id, text):
    return InlineQueryResultArticle(
        id=art_id,
        title="Поделиться ботом",
        thumb_url="https://telegra.ph/file/1f1fb2db55c9e7e758fb3.png",
        description="Нажмите, что-бы тегнуть бота",
        input_message_content=InputTextMessageContent(text),
    )


def services_status_article(art_id, text):
    return InlineQueryResultArticle(
        id=art_id,
        title="Cостояние сервисов",
        thumb_url="https://telegra.ph/file/1f1fb2db55c9e7e758fb3.png",
        description="Нажмите, что-бы узнать состояние всех сервисов",
        input_message_content=InputTextMessageContent(text),
    )


# edit later)
def about_worker_article(art_id, title, description, text):
    return InlineQueryResultArticle(
        id=art_id,
        title=title,
        description=description,
        input_message_content=InputTextMessageContent(text),
    )
