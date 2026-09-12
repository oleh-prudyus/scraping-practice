from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import db, scheduler
from .job import run_scrape_job


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    scheduler.start_scheduler()
    yield


app = FastAPI(title="Scraping Dashboard API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ToggleRequest(BaseModel):
    enabled: bool


class NotificationsRequest(BaseModel):
    telegram_token: str
    telegram_chat_id: str


@app.get("/status")
def get_status():
    return {
        "scheduler_enabled": scheduler.is_enabled(),
        "last_run": db.get_last_run(),
    }


@app.post("/toggle")
def toggle(body: ToggleRequest):
    scheduler.set_enabled(body.enabled)
    return {"scheduler_enabled": scheduler.is_enabled()}


@app.post("/run")
def trigger_run(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_scrape_job)
    return {"message": "Скрапінг запущено у фоні"}


@app.get("/data")
def get_data(limit: int = 200):
    return db.get_quotes(limit=limit)


@app.get("/notifications")
def get_notifications():
    token = db.get_setting("telegram_token", "")
    masked = f"{token[:4]}...{token[-4:]}" if len(token) > 8 else ("" if not token else "***")
    return {
        "telegram_token_set": bool(token),
        "telegram_token_masked": masked,
        "telegram_chat_id": db.get_setting("telegram_chat_id", ""),
    }


@app.post("/notifications")
def set_notifications(body: NotificationsRequest):
    db.set_setting("telegram_token", body.telegram_token)
    db.set_setting("telegram_chat_id", body.telegram_chat_id)
    return {"message": "Збережено"}
