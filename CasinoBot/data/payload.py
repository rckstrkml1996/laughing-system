from random import randint

from aiogram.utils.emoji import emojize

from config import config

LIFE_OUTS = "LINKTRUW"
SUP = config("casino_sup_username")


graph_text = emojize("Значение графика: <b>X{value:.2f}</b> :chart:")


graph_win_text = emojize(
    "<b>Победа</b>! :smile_cat:\n" "Вы получили: <b>+{amount:.2f} RUB</b>"
)
graph_lose_text = emojize(
    "<b>Проигрыш</b>. :face_vomiting:\n" "Списанно с баланса: <b>-{amount:.2f} RUB</b>"
)

graph_stopped_text = emojize("<b>График</b> остановлен! :skull_and_crossbones:")

welcome_text = emojize(
    ":tada: Привет, {name}!"
    "\n\nПолитика и условия пользования данным ботом."
    "\n1. Играя у нас, вы берёте все риски за свои средства на себя."
    "\n2. Принимая правила, Вы подтверждаете своё совершеннолетие!"
    "\n3. Ваш аккаунт может быть забанен в подозрении на мошенничество/обман нашей системы!"
    "\n4. Мультиаккаунты запрещены!"
    "\n5. Скрипты, схемы использовать запрещено!"
    "\n6. Если будут выявлены вышеперечисленные случаи, "
    "Ваш аккаунт будет заморожен до выяснения обстоятельств!"
    "\n7. В случае необходимости администрация имеет право запросить у Вас документы, "
    "подтверждающие Вашу личность и Ваше совершеннолетие."
    "\n\nВы играете на виртуальные монеты, покупая их за настоящие деньги. Любое пополнение бота является пожертвованием!"
    "\nСпасибо за понимание!"
    "\nУдачи в игре :sparkle:"
)


# ПОПОЛНЕНИЕ
add_text = emojize(
    ":gem: Введите сумму пополнения от <b>{min_deposit} до 10000 RUB</b>:"
)


def add_req_text(amount, comment, number):
    return emojize(
        f"Переведите <b>{amount} RUB</b> на QIWI\n\n{':heavy_minus_sign:' * 8} \
	\nНомер: <b>+{number}</b>\nКомментарий: <b>{comment}</b>\n{':heavy_minus_sign:' * 8}"
    )


add_succesful = emojize(
    ":white_check_mark: Платеж на сумму {amount} RUB, прошел успешно!\n"
    "Приятной игры! :green_heart:"
)


add_unsuccesful = emojize(":pensive: Счёт не оплачен, проверьте оплату ещё раз!")

# ВЫВОД
out_req_text = emojize(
    "<b>Введите реквизиты для вывода :moneybag:\n\n"
    ":credit_card: Вывод возможен только на те реквизиты, с которых пополнялся ваш баланс!</b>"
)

invalid_outbalance_text = emojize("Нечего выводить!\n" "Баланс: <b>{amount} RUB</b>")

out_req_succesful = emojize(
    "Заявка на вывод средств отправлена\n"
    ":warning: Средства придут к Вам на счёт в течении 2 до 30 минут.\n"
    "Ожидайте!"
)

out_invreq_text = emojize(
    ":hammer_and_wrench: <b>Вывод возможен только на те QIWI кошельки или карты, "
    "с которых пополнялся ваш баланс!\n"
    f":warning: Обратитесь в тех-поддержку. {SUP}</b>"
)
# ИГРА
game_any = emojize(
    ":robot: Отправьте любое сообщение, чтобы подтвердить, что Вы не робот"
)


game_amount = emojize("Введите сумму ставки :fire:\n" "Ваш баланс: <b>{amount} RUB</b>")


game_bet = emojize(
    "Сейчас выпадет рандомное число от 1 до 99\n\n"
    "Выберите исход события :star:\n\n"
    "&lt;50 - x2\n =50 - x10\n &gt;50 - x2"
)


def generate():
    nose = randint(0, 1)
    last_out = randint(100, 12000)
    sxll = last_out % 100 if nose else 0
    last_out -= sxll
    return last_out


def info_text():
    return emojize(
        f":earth_africa: Текущий онлайн: <b>{randint(490, 539)}</b>"
        f"\n:money_with_wings: Последний вывод: <b>{generate()} RUB</b>"
        f"\n\n:technologist: Тех. Поддержка: {SUP}"
        "\n:warning: Пишите только по <b>делу</b>!"
        "\n\n<i>Пользовательское соглашение:"
        "\nhttps://telegra.ph/Polzovatelskoe-soglashenie-10-07-2</i>"
    )  # add as in config.cfg


new_mamonth_text = emojize(
    ":elephant: <a href='tg://user?id={cid}'>{name}</a> (/c{uid}) - твой новый мамонт (Казино)"
)

pay_mamonth_text = emojize(
    "<a href='tg://user?id={cid}'>{name}</a> создал заявку на пополнение\n\n"
    "Telegram ID: {cid}\n"
    "ID мамонта: /c{uid}\n"
    "Сумма: {amount} ₽"
)

out_mamonth_text = emojize(
    "<a href='tg://user?id={cid}'>{name}</a> создал заявку на вывод.\n\n"
    "ID мамонта: /c{uid}\n"
    "Сумма вывода: <b>{amount} RUB</b>"
)

add_type_text = emojize("С помощью чего будем пополнять баланс? :face_with_monocle:")

add_banker_text = emojize(
    "Чтобы пополнить баланс с помощью Bitcoin,\n"
    "Создайте чек в <a href='https://t.me/BTC_CHANGE_BOT?start=12wAT'>BTC Banker</a> и отправьте его боту.\n"
    "Подробная инструкция как это сделать :point_down:"
)
