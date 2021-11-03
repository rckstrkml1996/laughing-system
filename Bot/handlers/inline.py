from secrets import token_hex

from aiogram.types import InlineQuery
from loguru import logger

from loader import dp, StatusNames
from utils import basefunctional
from data import texts
from data.inlineresults import (
    tagbot_article,
    services_status_article,
    about_worker_article,
)
from utils.executional import get_work_status, get_correct_str, get_info_about_worker


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    logger.debug(
        f"Inline Request with text: {inline_query.query} from {inline_query.from_user.id}"
    )
    if inline_query.query:
        finded = basefunctional.workers_by_username(inline_query.query)

        results = [
            about_worker_article(
                art_id=token_hex(6),
                title=worker.username,
                description=texts.about_worker_text.format(
                    status=StatusNames[worker.status],
                    profits=get_correct_str(
                        worker.profits.count(), "профит", "профита", "профитов"
                    ),
                    profits_sum=basefunctional.get_profits_sum(worker.id),
                ),
                text=get_info_about_worker(worker),
            )
            for worker in finded
        ]

        await inline_query.answer(results=results)
    else:
        bot_user = await dp.bot.get_me()
        standart_items = [
            tagbot_article(token_hex(6), f"Подавай заявку в @{bot_user.username}"),
            services_status_article(token_hex(6), get_work_status()),
        ]

        await inline_query.answer(results=standart_items)
        # don't forget to set cache_time=1 for testing (default is 300s or 5m)
