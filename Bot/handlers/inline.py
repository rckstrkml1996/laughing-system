import secrets

from peewee import fn
from aiogram.types import InlineQuery

from loader import dp
from models import Worker, Profit
from data import payload
from data.inlineresults import tagbot_article, services_status_article, about_worker_article
from utils.executional import get_work_status, get_correct_str, get_info_about_worker
from config import config, StatusNames


def correct_profits(n):
    return f'{n} {get_correct_str(n, "профит", "профита", "профитов")}'


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    if inline_query.query:
        # expression = fn.Lower(inline_query.query.lower() in Worker.username)
        finded = Worker.select().where(fn.Lower(Worker.username.contains(
            inline_query.query)), Worker.username_hide == False)

        results = [
            about_worker_article(
                art_id=secrets.token_hex(6),
                title=worker.username,
                description=payload.about_worker_text.format(
                    status=StatusNames[worker.status],
                    profits=correct_profits(len(worker.profits)),
                    profits_sum=sum(
                        map(lambda prft: prft.amount, worker.profits)
                    ),
                ),
                text=get_info_about_worker(worker)
            ) for worker in finded
        ]

        await inline_query.answer(results=results)
    else:
        bot_user = await dp.bot.get_me()
        standart_items = [
            tagbot_article(
                secrets.token_hex(6),
                f"Подавай заявку в @{bot_user.username}"
            ),
            services_status_article(
                secrets.token_hex(6),
                get_work_status()
            )
        ]

        await inline_query.answer(results=standart_items)
        # don't forget to set cache_time=1 for testing (default is 300s or 5m)
