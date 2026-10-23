from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_usuario
from app.core.security import criar_access_token
from app.crud.auth import autenticar_usuario
from app.database.connection import get_db
from app.models.usuario import Usuario
from app.schemas.auth import TokenResponse
from app.schemas.usuario import UsuarioResponse

router = APIRouter(
    prefix="/auth",
    tags=["autenticação"],
)


@router.post("/login", response_model=TokenResponse)
def login(
    dados: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = autenticar_usuario(
        db,
        email=dados.username,
        senha=dados.password,
    )

    token = criar_access_token(usuario.id)

    return TokenResponse(access_token=token)


@router.get("/me", response_model=UsuarioResponse)
def meu_perfil(
    usuario: Usuario = Depends(get_current_usuario),
):
    return usuario