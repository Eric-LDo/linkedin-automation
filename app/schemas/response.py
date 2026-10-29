from typing import List, Optional
from pydantic import BaseModel


class ConnectionRequest(BaseModel):
    """Representa um pedido de conexão enviado."""
    name: str
    profile_url: Optional[str] = None
    sent_at: Optional[str] = None


class MessageSent(BaseModel):
    """Representa uma mensagem enviada a um contato já conectado."""
    name: str
    profile_url: Optional[str] = None
    sent_at: Optional[str] = None
    message_preview: Optional[str] = None


class AutomationResponse(BaseModel):
    """Resposta completa da automação LinkedIn."""
    status: str
    message: Optional[str] = None

    # Lista de convites de conexão enviados nessa execução
    connection_requests_sent: List[ConnectionRequest] = []

    # Lista de mensagens enviadas nessa execução (apenas quem ainda não havia recebido)
    messages_sent: List[MessageSent] = []

    # Totais
    total_connection_requests: int = 0
    total_messages_sent: int = 0
