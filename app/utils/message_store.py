"""
Persistência simples em JSON para rastrear quem já recebeu mensagem.
Garante que a mesma pessoa nunca receba a mensagem duas vezes,
mesmo em execuções diferentes da API.

Formato do arquivo:
{
  "mensagens_enviadas": {
    "<profile_url_ou_nome_normalizado>": {
      "name": "João Silva",
      "profile_url": "https://linkedin.com/in/joaosilva",
      "sent_at": "2026-04-22T10:30:00"
    },
    ...
  }
}
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Arquivo de persistência fica em app/data/message_store.json
_STORE_PATH = Path(__file__).resolve().parents[2] / "app" / "data" / "message_store.json"


def _load_store() -> Dict:
    if _STORE_PATH.exists():
        try:
            return json.loads(_STORE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {"mensagens_enviadas": {}}
    return {"mensagens_enviadas": {}}


def _save_store(store: Dict) -> None:
    _STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    _STORE_PATH.write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8")


def _make_key(profile_url: Optional[str], name: str) -> str:
    """Cria uma chave única para identificar a pessoa."""
    if profile_url:
        # Normaliza a URL removendo query params e trailing slash
        key = profile_url.split("?")[0].rstrip("/").lower()
        return key
    # Fallback: usa nome normalizado
    return name.strip().lower()


def already_received_message(profile_url: Optional[str], name: str) -> bool:
    """Retorna True se a pessoa já recebeu a mensagem em alguma execução anterior."""
    store = _load_store()
    key = _make_key(profile_url, name)
    return key in store.get("mensagens_enviadas", {})


def mark_message_sent(profile_url: Optional[str], name: str) -> None:
    """Registra que a mensagem foi enviada para esta pessoa."""
    store = _load_store()
    key = _make_key(profile_url, name)
    store.setdefault("mensagens_enviadas", {})[key] = {
        "name": name,
        "profile_url": profile_url or "",
        "sent_at": datetime.now().isoformat(timespec="seconds"),
    }
    _save_store(store)


def list_all_messaged() -> Dict:
    """Retorna todos os registros de mensagens enviadas (para debug/auditoria)."""
    return _load_store().get("mensagens_enviadas", {})
