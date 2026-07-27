from fastapi import APIRouter, HTTPException
from app.models import UserCreate
from app.services.firestore_db import FirestoreDB

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/register")
def register_user(user_data: UserCreate):
    doc_id = FirestoreDB.create_document("users", user_data.model_dump())
    return {"message": "User registered successfully", "user_id": doc_id}

@router.put("/{user_id}/bind-line")
def bind_line_account(user_id: str, line_user_id: str):
    user = FirestoreDB.get_document("users", user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    FirestoreDB.update_document("users", user_id, {"line_user_id": line_user_id})
    return {"message": "LINE account linked successfully"}