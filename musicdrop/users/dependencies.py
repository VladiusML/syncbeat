from typing import Optional
from fastapi import Request, Depends 
from jose import jwt, JWTError
from exceptions import IncorrectTokenFormatException, TokenAbsentException, TokenExpiredException, UserIsNotPresentException
from musicdrop.config import settings
from datetime import datetime, timezone 
from musicdrop.users.dao import UsersDAO
from musicdrop.users.models import Users

def get_token(request: Request):
    token = request.cookies.get("musicdrop_access_token")
    if not token:
        return None   
    return token

async def get_current_user(token: str = Depends(get_token)):
    if token is None:
        raise TokenAbsentException
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.now(timezone.utc).timestamp():
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user

async def get_optional_current_user(token: Optional[str] = Depends(get_token)) -> Optional[Users]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None

    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.now(timezone.utc).timestamp():
        return None

    user_id: str = payload.get("sub")
    if not user_id:
        return None

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        return None

    return user