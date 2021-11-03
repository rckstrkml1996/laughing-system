from loguru import logger
from models import (
    Worker,
    EscortUser,
    EscortGirl,
    EscortPayment,
)


def get_worker_by_code(code: str) -> Worker:
    try:
        return Worker.get(uniq_key=code)
    except Worker.DoesNotExist:
        return None


def create_user(worker: Worker, chat_id: int, username: str, fullname: str):
    # if username is
    return EscortUser.create(
        owner=worker, cid=chat_id, username=username, fullname=fullname
    )


def create_payment(user, amount, comment):
    return EscortPayment.create(
        owner=user,
        amount=amount,
        comment=comment,
    )


def get_payment(payment_id: int) -> EscortPayment:
    try:
        return EscortPayment.get(id=payment_id)
    except EscortPayment.DoesNotExist:
        return None


def get_girl(girl_id: int) -> EscortGirl:
    try:
        return EscortGirl.get(id=girl_id)
    except EscortGirl.DoesNotExist as ex:
        logger.warning(f"{girl_id=} - {ex}")


def get_escort_girls_text_id(worker_id: int):
    girls = EscortGirl.select().where(
        (EscortGirl.for_all) | (EscortGirl.owner_id == worker_id)
    )  # need to return as list with strings in

    text_id = []

    for girl in girls[:15]:
        text_id.append(
            (f'{girl.name} {get_correct_str(girl.age, "Год", "Года", "Лет")}', girl.id)
        )

    return text_id


def get_escort_girl_count(worker_id: int):
    return (
        EscortGirl.select()
        .where((EscortGirl.for_all) | (EscortGirl.owner_id == worker_id))
        .count()
    )


def get_correct_str(num, str1, str2, str3):
    val = num % 100

    if val > 10 and val < 20:
        return f"{num} {str3}"
    else:
        val = num % 10
        if val == 1:
            return f"{num} {str1}"
        elif val > 1 and val < 5:
            return f"{num} {str2}"
        else:
            return f"{num} {str3}"
