from pydantic import BaseModel, Field

from .main import SumData


class AccountType(BaseModel):
    identifier: str = Field(alias='id')  # in api 'id'
    title: str


class Account(BaseModel):
    alias: str
    fsAlias: str
    bankAlias: str
    title: str
    hasBalance: bool
    currency: int
    accountType: AccountType = Field(alias='type')  # in api 'type'
    balance: SumData = None


class Accounts(BaseModel):
    accounts: list[Account]
