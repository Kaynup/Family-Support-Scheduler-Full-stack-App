from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional


class BillCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    due_date: str
    total_amount: float = Field(..., gt=0)
    category: Optional[str] = None
    status: str = Field(default="UNPAID")

    @field_validator('name')
    @classmethod
    def name_not_empty(class_, value):
        if not value or not str(value).strip():
            raise ValueError('name is required')
        return value.strip()

    @field_validator('due_date')
    @classmethod
    def due_date_not_past(class_, value):
        try:
            dt = date.fromisoformat(value)
        except ValueError:
            raise ValueError('due_date must be ISO format')
        if dt < date.today():
            raise ValueError('due_date cannot be in past')
        return value

    @field_validator('status')
    @classmethod
    def status_valid(class_, value):
        if value not in ('PAID', 'UNPAID'):
            raise ValueError("status must be 'PAID' or 'UNPAID'")
        return value


class BillUpdateRequest(BaseModel):
    status: str = Field(...)

    @field_validator('status')
    @classmethod
    def status_valid(class_, value):
        if value.upper().strip() not in ('PAID', 'UNPAID'):
            raise ValueError("status must be 'PAID' or 'UNPAID'")
        return value.upper().strip()


class BillResponse(BaseModel):
    id: int
    name: str
    creation_date: str
    due_date: str
    total_amount: float
    status: str
    category: Optional[str] = None

class BillListResponse(BaseModel):
    OK: bool = True
    total_count: int
    date: list[BillResponse]