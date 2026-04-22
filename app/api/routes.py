from typing import Union
from fastapi import APIRouter, HTTPException
from app.services.make_tasks import run_make_tasks
from app.schemas.request import AutomationRequest
router = APIRouter()

@router.get("/")
def health():
    return {"status": "ok"}

@router.post("/run")
def execute(payload: Union[AutomationRequest]):
    result = run_make_tasks(payload)
    if result.get("status") == "error":
        raise HTTPException(status_code=401, detail=result.get("message", "Erro ao executar automacao."))
    return result
