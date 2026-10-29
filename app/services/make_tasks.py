from app.bot.runner import run_Bot
from app.schemas.request import AutomationRequest


def run_make_tasks(payload: AutomationRequest) -> dict:
    """Delega a execução para o runner do bot e retorna o resultado como dict."""
    return run_Bot(payload)
