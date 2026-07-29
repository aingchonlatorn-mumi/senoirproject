from fastapi import APIRouter, HTTPException
from app.models import UserCreate
from app.services.firestore_db import FirestoreDB

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/register")
def register_user(user_data: UserCreate):
    try:
        clean_phone = str(user_data.phone).strip()
        data_dict = user_data.model_dump()
        data_dict["phone"] = clean_phone

        # เช็คว่ามีเบอร์นี้ในระบบหรือยัง
        existing = FirestoreDB.find_one_by_field("users", "phone", clean_phone)

        if existing:
            doc_id = existing["id"]
            # ถ้าระบบมี line_user_id อยู่แล้ว ให้คงค่าเดิมไว้ถ้าของใหม่เป็น None
            if not data_dict.get("line_user_id") and existing.get("line_user_id"):
                data_dict["line_user_id"] = existing["line_user_id"]

            FirestoreDB.update_document("users", doc_id, data_dict)
            return {"id": doc_id, "message": "User updated", **data_dict}

        # ถ้าเป็นผู้ใช้ใหม่ ให้สร้าง Document ใน Firestore
        doc_id = FirestoreDB.create_document("users", data_dict)
        return {"id": doc_id, "message": "User registered", **data_dict}

    except Exception as e:
        print(f"❌ REGISTER ERROR: {e}") # ดู Error ใน Terminal
        raise HTTPException(status_code=500, detail=str(e))