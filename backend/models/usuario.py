import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(100), nullable=False)

    email = Column(String(150), nullable=False, unique=True)

    senha = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow,onupdate=datetime.utcnow)

    tarefa = relationship(
        "Tarefas",
        back_populates="usuario",
        cascade="all, delete, delete-orphan",
    )