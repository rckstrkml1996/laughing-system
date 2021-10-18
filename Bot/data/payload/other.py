from aiogram.utils.emoji import emojize

# then remove it!!!\

worker_choice_one_plz = emojize(
    ":weary: Выбери один из <b>{status_len}</b> предложенных статусов!"
)

set_new_worker_status = emojize(
    ":see_no_evil: Установил новый статус <b>{status_name}</b> для {worker_link}"
)  # {worker_defenition.format(chat_id=diff_worker.cid, name=diff_worker.name)}
