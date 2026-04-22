from typing import Union

from fastapi import APIRouter, HTTPException

from app.services.make_tasks import run_make_tasks
from app.schemas.request import AutomationRequest
from app.schemas.response import AutomationResponse

router = APIRouter()


@router.get("/")
def health():
    return {"status": "ok"}


@router.post("/run", response_model=AutomationResponse)
def execute(payload: Union[AutomationRequest]) -> AutomationResponse:
    """
    Executa a automação do LinkedIn:
    - Faz login com as credenciais fornecidas.
    - Pesquisa pessoas pela query `search` e envia até `count` convites de conexão.
    - Navega para "Minhas Conexões" e envia mensagem personalizada para cada
      nova conexão que ainda não recebeu a mensagem (controle persistente).

    ### Retorno
    - **connection_requests_sent**: lista de pessoas que receberam convite nesta execução.
    - **messages_sent**: lista de pessoas que receberam a mensagem de boas-vindas nesta execução.
    - Pessoas que já receberam a mensagem em execuções anteriores são ignoradas.
    """
    result = run_make_tasks(payload)

    if result.get("status") == "error":
        raise HTTPException(
            status_code=500,
            detail=result.get("message", "Erro ao executar automação."),
        )

    return AutomationResponse(**result)
