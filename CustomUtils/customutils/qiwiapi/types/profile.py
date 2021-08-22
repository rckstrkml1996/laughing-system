from datetime import datetime

from pydantic import BaseModel  # , Field

from .main import SumData


class Nickname(BaseModel):
    nickname: str = None
    canChange: bool
    canUse: bool
    description: str = None


class IdentificationInfo(BaseModel):
    bankAlias: str
    identificationLevel: str
    passportExpired: bool


class SmsNotification(BaseModel):
    price: SumData
    enabled: bool
    active: bool
    endDate: datetime = None


class ContractInfo(BaseModel):
    blocked: bool = None
    contractId: int
    nickname: Nickname
    creationDate: datetime
    features: list = None
    identificationInfo: list[IdentificationInfo]
    smsNotification: SmsNotification = None


class AuthInfo(BaseModel):
    personId: int
    boundEmail: str = None
    ip: str = None
    lastLoginDate: datetime = None
    registrationDate: datetime


class UserInfo(BaseModel):
    defaultPayCurrency: int
    defaultPayAccountAlias: str
    email: str = None
    operator: str
    defaultPaySource: int = None
    language: str
    firstTxnId: int = None
    phoneHash: str
    integrationHashes: dict = None


class Profile(BaseModel):
    contractInfo: ContractInfo
    authInfo: AuthInfo
    userInfo: UserInfo
