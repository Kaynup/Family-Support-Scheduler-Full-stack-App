"""
Pydantic schemas for the bills domain.

BillCreateRequest  — validates incoming POST /bills/new payloads.
BillUpdateRequest  — validates incoming PUT /bills/{id} payloads.
BillResponse       — shape of a single bill in API responses.
BillListResponse   — shape of the list-bills API response envelope.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date
from typing import Optional, List
from enum import Enum


class BillStatus(str, Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"


class BillCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    due_date: date
    creation_date: Optional[date] = None
    total_amount: float = Field(..., gt=0)
    category: Optional[str] = None
    recurring_interval: str = Field(default="NONE")
    status: BillStatus = BillStatus.UNPAID

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("name is required and cannot be blank")
        return value

    @model_validator(mode="after")
    def creation_date_must_precede_due_date(self):
        if self.creation_date is not None:
            if self.creation_date > self.due_date:
                raise ValueError("creation_date cannot be later than due_date")
        if self.due_date < date.today():
            raise ValueError("due_date cannot be in the past")
        return self


class BillUpdateRequest(BaseModel):
    status: BillStatus


class BillResponse(BaseModel):
    id: int
    name: str
    creation_date: str
    due_date: str
    total_amount: float
    status: str
    category: Optional[str]
    recurring_interval: str
    is_expired: str


class BillListResponse(BaseModel):
    OK: bool
    total_count: int
    data: List[BillResponse]
