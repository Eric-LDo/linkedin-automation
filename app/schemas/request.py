from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.utils.string_utils import normalize_search_query

DEFAULT_SEARCH_QUERY = (
    '("tech recruiter" OR "RH recruiter" OR "recrutador" OR "recrutadora") '
    'AND ("Sao Jose do Rio Preto" OR "Sao Paulo")'
)

DEFAULT_SKILLS = "desenvolvimento de software, Python, automações e integrações"


class AutomationRequest(BaseModel):
    email: str = Field(
        default=None,
        description="Email do usuario para entrar no LinkedIn",
        examples=["seuemail@exemplo.com"],
    )
    password: str = Field(
        default=None,
        description="Senha do usuario para entrar no LinkedIn",
        examples=["suaSenha123"],
    )
    count: Optional[int] = Field(
        default=10,
        description="Quantidade máxima de convites de conexão a enviar nesta execução",
        examples=[10],
    )
    search: str = Field(
        default=DEFAULT_SEARCH_QUERY,
        description=(
            "Query de pesquisa de pessoas usada na barra de busca do LinkedIn. "
            "Exemplo: '(\"recrutador\" OR \"recruiter\") AND (\"São Paulo\")'"
        ),
        examples=[DEFAULT_SEARCH_QUERY],
    )
    my_skills: str = Field(
        default=DEFAULT_SKILLS,
        description=(
            "Suas principais habilidades/experiências que serão inseridas na mensagem "
            "enviada às novas conexões. Exemplo: 'Python, automação de processos e IA'."
        ),
        examples=[DEFAULT_SKILLS],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "",
                "password": "",
                "count": 10,
                "search": DEFAULT_SEARCH_QUERY,
                "my_skills": DEFAULT_SKILLS,
            }
        }
    }

    @field_validator("search", mode="before")
    @classmethod
    def sanitize_search(cls, value):
        return normalize_search_query(value, default_value=DEFAULT_SEARCH_QUERY)

    @field_validator("my_skills", mode="before")
    @classmethod
    def sanitize_skills(cls, value):
        if not value or str(value).strip() == "":
            return DEFAULT_SKILLS
        return str(value).strip()
