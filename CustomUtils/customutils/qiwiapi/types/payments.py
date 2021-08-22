from datetime import datetime

from pydantic import BaseModel, Field

from .main import SumData


class TransactionInfo(BaseModel):
    providerId: int = Field(alias='id')
    shortName: str = None
    longName: str = None
    logoUrl: str = None
    description: str = None
    keys: str = None
    siteUrl: str = None


class Transaction(BaseModel):
    txnId: int
    personId: int
    date: datetime
    errorCode: int
    error: str = None
    trnsType: str = Field(alias='type')  # in api 'type'
    status: str
    statusText: str
    trmTxnld: str = None
    account: str
    transactionSum: SumData = Field(alias='sum')
    commision: SumData = None
    total: SumData
    provider: TransactionInfo = None
    source: TransactionInfo = None
    comment: str = None
    currencyRate: int


class Payments(BaseModel):
    data: list[Transaction]
    nextTxnId: int = None
    nextTxnDate: datetime = None
