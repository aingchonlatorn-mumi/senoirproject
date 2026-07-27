from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- Users ---
class UserCreate(BaseModel):
    name: str
    phone: str
    device_id: str
    line_user_id: Optional[str] = None

class UserResponse(UserCreate):
    id: str
    created_at: datetime

# --- Medicines ---
class MedicineCreate(BaseModel):
    user_id: str
    name: str
    total_pills: int
    remaining_pills: int
    expire_date: str  # เช่น "2026-12-31"

class MedicineResponse(MedicineCreate):
    id: str
    created_at: datetime

# --- Schedules ---
class ScheduleCreate(BaseModel):
    user_id: str
    medicine_id: str
    time: str  # เช่น "08:00"
    days_of_week: List[str]  # e.g., ["mon", "tue"] หรือ ["daily"]
    dose_amount: int
    active: bool = True

class ScheduleResponse(ScheduleCreate):
    id: str