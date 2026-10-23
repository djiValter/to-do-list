from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TarefaCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    descricao: str
    usuario_id: int = Field(gt=0)


class TarefaUpdate(BaseModel):
    titulo: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    descricao: str | None = None
    concluida: bool | None = None


class TarefaResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    concluida: bool
    usuario_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)