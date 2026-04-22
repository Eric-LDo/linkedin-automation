from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.utils.string_utils import normalize_search_query

DEFAULT_SEARCH_QUERY = '("tech recruiter" OR "RH recruiter" OR "recrutador" OR "recrutadora") AND ("Sao Jose do Rio Preto" OR "Sao Paulo")'


class AutomationRequest(BaseModel):
    email: str = Field(
        default=None,
        description="Email do usuario para entrar no linkedin",
        examples=["teste@testemail.com"],
    )
    password: str = Field(
        default=None,
        description="Senha do usuario para entrar no linkedin",
        examples=["123senha"],
    )
    count: Optional[int] = Field(
        default=10,
        description="Quantidade de conexoes por request",
        examples=[10],
    )
    search: str = Field(
        default=DEFAULT_SEARCH_QUERY,
        description='("tech recruiter" OR "RH recruiter" OR "recrutador" OR "recrutadora") AND ("Sao Jose do Rio Preto" OR "Sao Paulo")',
        examples=["(\"tech recruiter\" OR \"RH recruiter\" OR \"recrutador\" OR \"recrutadora\") AND (\"Sao Jose do Rio Preto\" OR \"Sao Paulo\")"],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "",
                "password": "",
                "count": 10,
                "search": DEFAULT_SEARCH_QUERY,
            }
        }
    }

    @field_validator("search", mode="before")
    @classmethod
    def sanitize_search(cls, value):
        return normalize_search_query(value, default_value=DEFAULT_SEARCH_QUERY)
