from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta, timezone
import jwt


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def password_verfiy(password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed_password)


def create_access_token(
    data: dict, SECRET_KEY: str, ALGORITHM: str, expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=1)
    to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
