from datetime import datetime

from pydantic import BaseModel  # , Field

from .main import SumData


class TotalPayments(BaseModel):
    incomingTotal: list[SumData]
    outgoingTotal: list[SumData]
