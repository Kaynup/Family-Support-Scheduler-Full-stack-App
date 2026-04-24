from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date
from typing import Optional
from enum import Enum


class BillStatus(str, Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"

class BillCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    due_date: date
    creation_date: date
    total_amount: float = Field(..., gt=0)
    category: Optional[str] = None
    status: BillStatus = BillStatus.UNPAID

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('name is required')
        return value

    @model_validator(mode='after')
    def validate_dates(self):
        if self.creation_date > self.due_date:
            raise ValueError('creation_date cannot be greater than due_date')
        if self.due_date < date.today():
            raise ValueError('due_date cannot be in past')
        return self

class BillUpdateRequest(BaseModel):
    status: BillStatus

class BillResponse(BaseModel):
    id: int
    name: str
    creation_date: date
    due_date: date
    total_amount: float
    status: BillStatus
    category: Optional[str] = None

class BillListResponse(BaseModel):
    OK: bool = True
    total_count: int
    data: list[BillResponse]