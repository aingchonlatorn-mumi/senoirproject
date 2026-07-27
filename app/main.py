from fastapi import FastAPI
from app.routes import users, medicines, schedules, line_webhook

app = FastAPI(title="Smart Medicine Box API")

app.include_router(users.router)
app.include_router(medicines.router)
app.include_router(schedules.router)
app.include_router(line_webhook.router)

@app.get("/")
def root():
    return {"status": "Backend Server Ready!"}