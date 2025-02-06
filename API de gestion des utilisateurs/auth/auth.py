import bcrypt
from datetime import timedelta, datetime
from jose import JWTError, jwt
from typing import Optional
from cryptography.fernet import Fernet
from passlib.context import CryptContext

SECRET_KEY=b'VwHry2S_bV2IKQUstIAO0TPLmyV0Pv3XooqzmGm14yY='
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt_and_hash_password(password: str, encryption_key: bytes=SECRET_KEY) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    fernet = Fernet(encryption_key)
    encrypted_password = fernet.encrypt(hashed_password)
    return encrypted_password.decode('utf-8')

def decrypt_password(encrypted_password: str, encryption_key: bytes) -> str:
    fernet = Fernet(encryption_key)
    hashed_password = fernet.decrypt(encrypted_password.encode('utf-8'))
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def check_password(encrypted_password, password, encryption_key=SECRET_KEY):
    hashed = decrypt_password(encrypted_password, encryption_key)
    result = verify_password(password, hashed)
    return result

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def jwt_create(username: str) -> dict:
    return {
        "access": create_access_token(username),
        'refresh': create_refresh_token(username),
        'type': 'Bearer',
        'username': username
    }


