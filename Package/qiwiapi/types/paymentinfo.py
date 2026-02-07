from pydantic import BaseModel, Field

from .main import SumData

class PaymentState(BaseModel):
    code: str


class PaymentTransaction(BaseModel):
    transactionId: int = Field(alias='id')
    state: PaymentState


class PaymentFields(BaseModel):
    account: str


class PaymentInfo(BaseModel):
    paymentId: int = Field(alias='id')
    terms: str
    fields: PaymentFields
    paymentSum: SumData = Field(alias='sum')
    transaction: PaymentTransaction
    source: str
    comment: str = None
