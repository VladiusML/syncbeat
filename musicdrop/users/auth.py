from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone 
from jose import jwt
 
from musicdrop.config import settings
from musicdrop.users.dao import UsersDAO 

pwd_content = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def get_password_hash(password: str) -> str: 
    return pwd_content.hash(password)

def verifiy_password(plain_password, hashed_password) -> bool:
    return pwd_content.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = 30)
    to_encode.update({"exp":expire}) 
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )

    return encoded_jwt 

async def authenticate_user(username: str, password: str) :
    user = await UsersDAO.find_one_or_none(username = username)
    if not user and not verifiy_password(password, user.hashed_password):
        return None
    return user