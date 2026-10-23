from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security import hash_password
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate


def criar_usuario(db: Session, dados: UsuarioCreate):
    usuario_existe = (
        db.query(Usuario)
        .filter(Usuario.email == dados.email)
        .first()
    )

    if usuario_existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um utilizador com este email.",
        )

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=hash_password(dados.senha),
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


def listar_usuarios(
    db: Session,
    skip: int = 0,
    limit: int = 100,
):
    return (
        db.query(Usuario)
        .order_by(Usuario.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def buscar_usuario(db: Session, usuario_id: int):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilizador não encontrado.",
        )

    return usuario


def atualizar_usuario(
    db: Session,
    usuario_id: int,
    dados: UsuarioUpdate,
):
    usuario = buscar_usuario(db, usuario_id)

    campos = dados.model_dump(exclude_unset=True)

    # Os campos podem ser omitidos, mas não podem receber null.
    for campo, valor in campos.items():
        if valor is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"O campo '{campo}' não pode ser nulo.",
            )

    if "email" in campos:
        email_em_uso = (
            db.query(Usuario)
            .filter(
                Usuario.email == campos["email"],
                Usuario.id != usuario_id,
            )
            .first()
        )

        if email_em_uso:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe outro utilizador com este email.",
            )

    if "senha" in campos:
        campos["senha"] = hash_password(campos["senha"])

    for campo, valor in campos.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)

    return usuario


def apagar_usuario(db: Session, usuario_id: int):
    usuario = buscar_usuario(db, usuario_id)

    db.delete(usuario)
    db.commit()

    return {"detail": "Utilizador apagado com sucesso."}