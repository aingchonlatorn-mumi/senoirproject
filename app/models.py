from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    phone: str
    device_id: str
    line_user_id: Optional[str] = None

class MedicineCreate(BaseModel):
    user_id: str
    name: str
    total_pills: int
    remaining_pills: int
    expire_date: str  # เช่น "2026-12-31"

class ScheduleCreate(BaseModel):
    user_id: str
    medicine_id: str
    time: str  # เช่น "08:00"
    days_of_week: List[str]  # e.g., ["mon", "tue"] หรือ ["daily"]
    dose_amount: int
    active: bool = True

class UserRegister(BaseModel):
    name: str
    phone: str
    device_id: str
    line_user_id: Optional[str] = None