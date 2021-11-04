from aiogram.utils.emoji import emojize


escort_text = emojize(
    ":green_heart: <b>Эскортик</b>\n\n"
    "Твой код: <code>{worker_id}</code>\n"
    "Скам бот - @{escort_username}\n"
    "Тех. поддержка - @{escort_sup_username}\n\n"
    "<a href='t.me/{escort_username}?start={worker_id}'>Реферальная ссылка</a>\n\n"
    "Мануалы - @{reviews_link}\n\n"
    "/info [<code>ID мамонта]</code> - инфо о мамонте\n"
    "/del [<code>ID мамонта]</code> - удалить мамонта\n"
    "/msg [<code>ID мамонта]</code>;[<code>Сообщение]</code> - сообщение от бота\n"
)

all_esc_mamonths_text = emojize(
    ":kiss: У тебя <b>{mamonths_plur}</b>:\n\n"
    "{all_mamonths}\n\n"
    "Обновлено в <i>{time}</i>"
)

esc_mamonth_info_text = emojize(
    "(/e{mid}) - <a href='tg://user?id={cid}'>{name}</a> - <b>{balance} RUB</b>"
)

escort_new_name = emojize(":tipping_hand_woman: <b>Напишите</b> имя вашей девочки")

escort_new_description = emojize(
    ":raising_hand_woman: <b>Напишите</b> инфо о вашей девочке, пример:\n\n"
    "Молодая, гибкая, красивая) Встречу наедине гарантирую!Все фото мои и полностью соответствуют!!!"
    "Приходи ко мне и я окуну тебя в мир соблазна, где нам никто не сможет помешать."
)

escort_new_service = emojize(
    ":raising_hand_woman: <b>Напишите</b> список услуг вашей девочки, пример:\n\n"
    "Основное - классика, анал. Минет - с резинкой, без резинки, кунилингус."
    "Финиш - в рот, на лицо, на грудь. Стриптиз - не профи. Массаж - классический."
)

escort_new_age = emojize(
    ":raising_hand_woman: <b>Введите</b> возраст вашей девочки, пример:\n\n21"
)

escort_new_price = emojize(
    ":raising_hand_woman: <b>Введите</b> стоимость услуг за 1 час, пример:\n\n3100"
)

escort_new_photos = emojize(
    ":raising_hand_woman: <b>Пришли</b> до 5 фоток твоей девочки:"
)

escort_new_photo_added = emojize(
    ":raising_hand_woman: Фото добавлено, если хочешь добавить ещё фото, пришли мне его Если нет, нажми на кнопку создать анкету"
)

escort_mamonth_info = emojize(
    "{smile} Мамонт <i>e{uid}</i>\n\n"
    "Telegram ID: [<code>{chat_id}</code>]\n"
    "ID Мамонта: /e{uid}\n"
    "Аккаунт: <a href='tg://user?id={chat_id}'>{name}</a>\n\n"
    "Обновлено в <i>{time}</i>"
)
