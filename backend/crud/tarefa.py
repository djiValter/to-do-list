from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.tarefa import Tarefa
from models.usuario import Usuario
from schemas.tarefa import TarefaCreate, TarefaUpdate


def criar_tarefa(db: Session, dados: TarefaCreate):
    usuario = (
        db.query(Usuario)
        .filter(Usuario.id == dados.usuario_id)
        .first()
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilizador não encontrado.",
        )

    tarefa = Tarefa(**dados.model_dump())

    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)

    return tarefa


def listar_tarefas(
    db: Session,
    usuario_id: int,
    skip: int = 0,
    limit: int = 100,
):
    return (
        db.query(Tarefa)
        .filter(Tarefa.usuario_id == usuario_id)
        .order_by(Tarefa.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def buscar_tarefa(
    db: Session,
    tarefa_id: int,
    usuario_id: int,
):
    tarefa = (
        db.query(Tarefa)
        .filter(
            Tarefa.id == tarefa_id,
            Tarefa.usuario_id == usuario_id,
        )
        .first()
    )

    if tarefa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada.",
        )

    return tarefa


def atualizar_tarefa(
    db: Session,
    tarefa_id: int,
    usuario_id: int,
    dados: TarefaUpdate,
):
    tarefa = buscar_tarefa(db, tarefa_id, usuario_id)

    campos = dados.model_dump(exclude_unset=True)

    for campo, valor in campos.items():
        if valor is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"O campo '{campo}' não pode ser nulo.",
            )

    for campo, valor in campos.items():
        setattr(tarefa, campo, valor)

    db.commit()
    db.refresh(tarefa)

    return tarefa


def apagar_tarefa(
    db: Session,
    tarefa_id: int,
    usuario_id: int,
):
    tarefa = buscar_tarefa(db, tarefa_id, usuario_id)

    db.delete(tarefa)
    db.commit()

    return {"detail": "Tarefa apagada com sucesso."}