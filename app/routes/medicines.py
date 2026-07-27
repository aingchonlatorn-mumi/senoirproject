from fastapi import APIRouter
from app.models import MedicineCreate
from app.services.firestore_db import FirestoreDB

router = APIRouter(prefix="/api/medicines", tags=["Medicines"])

@router.post("/")
def add_medicine(medicine: MedicineCreate):
    med_id = FirestoreDB.create_document("medicines", medicine.model_dump())
    return {"message": "Medicine added", "medicine_id": med_id}