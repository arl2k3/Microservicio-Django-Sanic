from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class PurchaseCreateSchema(BaseModel):
    name: str
    amount: float
    commission_rate: float

class PurchaseUpdateSchema(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    commission_rate: Optional[float] = None

class PurchaseResponseSchema(BaseModel):
    id: str
    name: str
    amount: float
    commission_rate: float
    commission: float