import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("A variável DATABASE_URL não está definida no .env.")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db(): //Fornece uma sessão à rota e fecha-a quando a requisição termina.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()