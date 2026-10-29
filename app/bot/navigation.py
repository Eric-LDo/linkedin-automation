from typing import Union

from playwright.sync_api import Page

from app.schemas.request import AutomationRequest
from app.schemas.response import AutomationResponse
from app.bot.conect_recruiter import search_recruiters
from app.bot.message_sender import send_messages_to_new_connections

LOGIN_URL = (
    "https://www.linkedin.com/login/pt"
    "?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
)
FEED_URL_PREFIX = "https://www.linkedin.com/feed"


def navigate_and_connect(
    page: Page,
    payload: Union[AutomationRequest],
) -> AutomationResponse:
    """
    Orquestra todo o fluxo:
    1. Login no LinkedIn.
    2. Pesquisa e envia convites de conexão (até payload.count pessoas).
    3. Navega até "Minhas Conexões" e envia mensagem inicial para quem
       acabou de aceitar e ainda não recebeu a mensagem.
    4. Retorna AutomationResponse com as duas listas.
    """

    # ── 1. Login ──────────────────────────────────────────────────────────────
    login(page, payload)

    # ── 2. Envio de convites ──────────────────────────────────────────────────
    connection_requests = search_recruiters(page, payload.search, payload.count)

    # ── 3. Envio de mensagens para conexões já aceitas ────────────────────────
    messages_sent = send_messages_to_new_connections(page, payload.my_skills)

    # ── 4. Monta resposta ─────────────────────────────────────────────────────
    return AutomationResponse(
        status="success",
        message="Automação concluída com sucesso.",
        connection_requests_sent=connection_requests,
        messages_sent=messages_sent,
        total_connection_requests=len(connection_requests),
        total_messages_sent=len(messages_sent),
    )


def login(page: Page, payload: Union[AutomationRequest]) -> None:
    print("Iniciando login...")
    page.goto(LOGIN_URL, wait_until="domcontentloaded")
    page.locator("#username").fill(payload.email)
    page.locator("#password").fill(payload.password)
    page.get_by_role("button", name="Entrar", exact=True).click()
    page.wait_for_timeout(3000)

    current_url = page.url
    print(f"URL atual após login: {current_url}")

    if current_url.startswith(FEED_URL_PREFIX):
        print("Login realizado com sucesso.")
        return

    raise ValueError("Login inválido ou bloqueado pelo LinkedIn.")
