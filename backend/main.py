from fastapi import FastAPI

from app.routers.usuario import router as usuario_router
from app.routers.tarefa import router as tarefa_router
from app.routers.auth import router as auth_router

app = FastAPI(title="API de Tarefas")

app.include_router(
    usuario_router,
    tarefa_router,
    auth_router,
)