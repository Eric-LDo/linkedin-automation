# linkedin-automation
Base de API em Python para rotinas de automacao no LinkedIn de forma mais segura.

## O que esta implementado
- API com `FastAPI`
- Endpoint de saude: `GET /api/v1/health`
- Endpoint de rotina: `POST /api/v1/automation/linkedin/profile-snapshot`
- Integracao inicial com LinkedIn API via `OAuth access_token` (sem receber senha em texto puro)
- Testes basicos com `pytest`

## Por que nao usar login/senha na API
Para reduzir risco de vazamento de credenciais e abuso de conta, a base foi feita com token OAuth.
Assim, a API recebe apenas token temporario com escopo controlado.

## Como executar
1. Crie e ative um ambiente virtual.
2. Instale dependencias:

```bash
pip install -r requirements.txt
```

3. Suba a API:

```bash
uvicorn app.main:app --reload
```

4. Teste o healthcheck:

```bash
curl http://127.0.0.1:8000/api/v1/health
```

## Exemplo da rotina

```bash
curl -X POST http://127.0.0.1:8000/api/v1/automation/linkedin/profile-snapshot \
  -H "Content-Type: application/json" \
  -d "{\"access_token\":\"SEU_ACCESS_TOKEN\",\"dry_run\":true}"
```

## Executar testes

```bash
pytest
```
