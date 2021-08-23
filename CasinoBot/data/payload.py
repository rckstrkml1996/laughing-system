from random import randint

from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import quote_html

# from config import SUP, LIFE_OUTS, MINIK
SUP = "SUPPER"
LIFE_OUTS = "LINKTRUW"
MINIK = "100"
# политика конф. при старте бота для новых


def welcome_text(first): return emojize(quote_html(f":tada: Привет, {first}! \
	\n\nПолитика и условия пользования данным ботом. \
	\n1. Играя у нас, вы берёте все риски за свои средства на себя. \
	\n2. Принимая правила, Вы подтверждаете своё совершеннолетие! \
	\n3. Ваш аккаунт может быть забанен в подозрении на мошенничество/обман нашей системы! \
	\n4. Мультиаккаунты запрещены! \
	\n5. Скрипты, схемы использовать запрещено! \
	\n6. Если будут выявлены вышеперечисленные случаи, Ваш аккаунт будет заморожен до выяснения обстоятельств! \
	\n7. В случае необходимости администрация имеет право запросить у Вас документы, подтверждающие Вашу личность \
	и Ваше совершеннолетие. \
	\n\nВы играете на виртуальные монеты, покупая их за настоящие деньги. Любое пополнение бота является пожертвованием! \
	\nСпасибо за понимание! \
	\nУдачи в игре."))


# ПОПОЛНЕНИЕ
add_text = emojize(f":gem: Введите сумму пополнения от <b>{MINIK} RUB</b>: \
	\n(например, если вы хотите пополнить баланс на <b>1000 RUB</b>, отправьте в чат сообщение ‘1000’, без кавычек)")


def add_req_text(amount, comment, number): return emojize(f"Переведите <b>{amount} RUB</b> на QIWI\n\n{':heavy_minus_sign:' * 8} \
	\nНомер: <b>+{number}</b>\nКомментарий: <b>{comment}</b>\n{':heavy_minus_sign:' * 8}")


def add_succesful(amount): return emojize(quote_html(f":white_check_mark: Платеж на сумму {amount} RUB, прошел успешно! \
	\nПриятной игры! :green_heart:")
                                          )


add_unsuccesful = emojize(
    ":pensive: Счёт не оплачен, проверьте оплату ещё раз!")

# ВЫВОД
out_req_text = emojize("Введите реквизиты для вывода :iphone:\
	\n:warning: Вывод возможен только на реквизиты, с которых пополнялся Ваш баланс!")

out_req_succesful = emojize("Заявка на вывод средств отправлена \
	\n:warning: Средства придут к Вам на счёт в течении от 2 до 30 минут.\nОжидайте!")

out_invreq_text = emojize(f":hammer_and_wrench: Упс.. \
	\nКажется у вас не пройдена верификация \
	\n:warning: Прошу обратится в Тех. Поддержку @{SUP}")

# ИГРА
game_any = emojize(
    ":robot: Отправьте любое сообщение, чтобы подтвердить, что Вы не робот")


def game_amount(balance): return emojize(f"Введите сумму ставки :fire: \
	\nВаш баланс: <b>{balance} RUB</b>")


game_bet = quote_html(emojize("Сейчас выпадет рандомное число от 1 до 99 \
	\n\nВыберите исход события :star: \
	\n <50 - x2\n =50 - x10\n >50 - x2"))


def generate():
    nose = randint(0, 1)
    last_out = randint(100, 12000)
    sxll = last_out % 100 if nose else 0
    last_out -= sxll
    return last_out


def info_text(): return emojize(f"Лицензия на предоставление услуг :point_up_2: \
	\n\n:earth_africa: Текущий онлайн: <b>{randint(420, 450)}</b> \
	\n:money_with_wings: Последний вывод: <b>{generate()} RUB</b> \
	\n:fire: Лайв выводы: {LIFE_OUTS} \
	\n\nПо любым вопросам, Тех. Поддержка: @{SUP} \
	\n:warning: Пишите сразу по делу! \
	\n\n<i>Пользовательское соглашение: \
	\nhttps://telegra.ph/Polzovatelskoe-soglashenie-03-17</i>")
