from fastapi import APIRouter
from app.services.make_tasks import run_make_tasks
router = APIRouter()

@router.get("/")
def health():
    return {"status": "ok"}

@router.post("/run")
def execute(payload: dict):
    return run_make_tasks(payload)
