import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database.base import Base


class Tarefa(Base):
    __tablename__ = 'tarefas'

    id = Column(Integer, primary_key=True, index=True)

    titulo = Column(String(100), nullable=False)

    descricao = Column(Text, nullable=False)

    concluida = Column(Boolean, nullable=False, default=False)

    usuario_id = Column(Integer, ForeignKey('usuarios.id'))

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = relationship(
        "Usuario",
        back_populates="tarefas",
    )