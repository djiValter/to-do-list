from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class UsuarioUpdate(BaseModel):
    nome: str  | None = None
    email: EmailStr | None = None
    senha: str | None = None



class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

