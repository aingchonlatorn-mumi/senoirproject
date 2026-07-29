from fastapi import FastAPI, HTTPException
from app.routes import users, medicines, schedules, line_webhook
from app.services.firestore_db import FirestoreDB

app = FastAPI(title="Smart Medicine Box API")

app.include_router(users.router)
app.include_router(medicines.router)
app.include_router(schedules.router)
app.include_router(line_webhook.router)

@app.get("/")
def root():
    return {"status": "Backend Server Ready!"}

@app.get("/api/users/line/{line_id}")
def get_user_by_line_id(line_id: str):
    user = FirestoreDB.find_one_by_field("users", "line_user_id", line_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
