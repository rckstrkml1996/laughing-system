import re
from typing import Optional
from hashlib import md5
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# import jwt
from qiwiapi.types import Payments

from customutils.models import QiwiPayment
from loader import app


# post /token does not exist))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# token gets like Authorization: Bearer "TOKEN"


@app.post("/new_payments")
async def new(payments: Payments, token: str = Depends(oauth2_scheme)):
    tokens = []
    if token in tokens:  # tokes suppose to be nahui qiwi tokenom
        pass
    # print(payments.data[0].personId)
