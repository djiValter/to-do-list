from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verificar_senha
from app.models.usuario import Usuario


def autenticar_usuario(
    db: Session,
    email: str,
    senha: str,
) -> Usuario:
    usuario = (
        db.query(Usuario)
        .filter(Usuario.email == email)
        .first()
    )

    if usuario is None:
        raise credenciais_invalidas()

    if not verificar_senha(senha, usuario.senha):
        raise credenciais_invalidas()

    return usuario


def credenciais_invalidas() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email ou senha incorretos.",
        headers={"WWW-Authenticate": "Bearer"},
    )