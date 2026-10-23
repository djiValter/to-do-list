from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.crud.usuario import (
    criar_usuario,
    listar_usuarios,
    buscar_usuario,
    atualizar_usuario,
    listar_usuarios,
    apagar_usuario,
)

from app.database.connection import get_db

from app.schemas import (
   UsuarioResponse,
   UsuarioCreate,
   UsuarioUpdate,
)

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

# ======================================================
#                       POST
# ======================================================
@router.post("/", response_model=UsuarioResponse, status_code=HTTP_201_CREATED,)
def creat(dados: UsuarioCreate, db: Session = Depends(get_db)):
    return criar_usuario(db, dados)


# ======================================================
#                       GET
# ======================================================
@router.get("/", response_model=list[UsuarioResponse])
def list_all(skip: int = Query(default=0, ge=0), limit: int = Query(default=100, ge=1, le=100), db: Session = Depends(get_db),):
    return listar_usuarios(db, skip=skip, limit=limit)


# ======================================================
#                       GET/ID
# ======================================================
@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar( usuario_id: int, db: Session = Depends(get_db),):
    return buscar_usuario(db, usuario_id)


# ======================================================
#                       PUT
# ======================================================
@router.patch("/{usuario_id}", response_model=UsuarioResponse)
def atualizar(
    usuario_id: int,
    dados: UsuarioUpdate,
    db: Session = Depends(get_db),
):
    return atualizar_usuario(db, usuario_id, dados)


# ======================================================
#                       DELETE
# ======================================================
@router.delete("/{usuario_id}")
def apagar(
    usuario_id: int,
    db: Session = Depends(get_db),
):
    return apagar_usuario(db, usuario_id)
