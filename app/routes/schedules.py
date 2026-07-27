from fastapi import APIRouter
from app.models import ScheduleCreate
from app.services.firestore_db import FirestoreDB

router = APIRouter(prefix="/api/schedules", tags=["Schedules"])

@router.post("/")
def add_schedule(schedule: ScheduleCreate):
    sched_id = FirestoreDB.create_document("schedules", schedule.model_dump())
    return {"message": "Schedule created", "schedule_id": sched_id}