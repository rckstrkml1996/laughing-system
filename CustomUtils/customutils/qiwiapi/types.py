from datetime import datetime

from pydantic import BaseModel, Field


class AccountType(BaseModel):
    identifier: str = Field(alias='id')  # in api 'id'
    title: str


class Balance(BaseModel):
    amount: int
    currency: int


class Account(BaseModel):
    alias: str
    fsAlias: str
    bankAlias: str
    title: str
    hasBalance: bool
    currency: int
    accountType: AccountType = Field(alias='type')  # in api 'type'
    balance: Balance = None


class Accounts(BaseModel):
    accounts: list[Account]


class TransactionSumData(BaseModel):
    amount: int
    currency: int


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
    transactionSum: TransactionSumData = Field(alias='sum')
    commision: TransactionSumData = None
    total: TransactionSumData
    provider: TransactionInfo = None
    source: TransactionInfo = None
    comment: str = None
    currencyRate: int


class Payments(BaseModel):
    data: list[Transaction]
    nextTxnId: int = None
    nextTxnDate: datetime = None


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
    paymentSum: TransactionSumData = Field(alias='sum')
    transaction: PaymentTransaction
    source: str
    comment: str = None
