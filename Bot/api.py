from fastapi import Depends

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from customutils.qiwiapi.types import Transaction

from config import config
from loader import app, dp


# post /token does not exist))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# token gets like Authorization: Bearer "TOKEN"


@app.post("/new_transaction")
async def new(
    transaction: Transaction, status: str, token: str = Depends(oauth2_scheme)
):
    print(status)

    tokens = config("qiwi_tokens")
    if isinstance(tokens, list):
        tokens = [tokens]

    if token not in tokens:  # tokes suppose to be nahui qiwi tokenom
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid qiwi token"
        )

    await dp.bot.send_message(config("admins_chat"), "Новая транзакция в киви епта")

    print(transaction)
