from passlib.hash import pbkdf2_sha256

def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def password_verfiy(password: str, hashed_password: str) -> bool:
  return pbkdf2_sha256.verify(password, hashed_password)