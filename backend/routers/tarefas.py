from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.crud.tarefa import (
    apagar_tarefa,
    atualizar_tarefa,
    buscar_tarefa,
    criar_tarefa,
    listar_tarefas,
)
from app.database.connection import get_db
from app.schemas.tarefa import (
    TarefaCreate,
    TarefaResponse,
    TarefaUpdate,
)

router = APIRouter(
    prefix="/tarefas",
    tags=["tarefas"],
)


@router.post(
    "/",
    response_model=TarefaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar(
    dados: TarefaCreate,
    db: Session = Depends(get_db),
):
    return criar_tarefa(db, dados)


@router.get("/", response_model=list[TarefaResponse])
def listar(
    usuario_id: int = Query(gt=0),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return listar_tarefas(
        db,
        usuario_id=usuario_id,
        skip=skip,
        limit=limit,
    )


@router.get("/{tarefa_id}", response_model=TarefaResponse)
def buscar(
    tarefa_id: int,
    usuario_id: int = Query(gt=0),
    db: Session = Depends(get_db),
):
    return buscar_tarefa(
        db,
        tarefa_id=tarefa_id,
        usuario_id=usuario_id,
    )


@router.patch("/{tarefa_id}", response_model=TarefaResponse)
def atualizar(
    tarefa_id: int,
    dados: TarefaUpdate,
    usuario_id: int = Query(gt=0),
    db: Session = Depends(get_db),
):
    return atualizar_tarefa(
        db,
        tarefa_id=tarefa_id,
        usuario_id=usuario_id,
        dados=dados,
    )


@router.delete("/{tarefa_id}")
def apagar(
    tarefa_id: int,
    usuario_id: int = Query(gt=0),
    db: Session = Depends(get_db),
):
    return apagar_tarefa(
        db,
        tarefa_id=tarefa_id,
        usuario_id=usuario_id,
    )