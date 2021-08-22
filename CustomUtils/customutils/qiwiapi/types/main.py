from pydantic import BaseModel


class SumData(BaseModel):
    amount: int
    currency: int
