import os
import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não está definida no .env.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str :
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def criar_access_token(usuario_id: int) -> str:
    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados = {
        "sub": str(usuario_id),
        "exp": expiracao,
    }

    return jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
