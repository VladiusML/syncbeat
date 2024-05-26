from musicdrop.database import async_session_maker
from musicdrop.dao.base import BaseDAO
from musicdrop.users.models import Users

from sqlalchemy import select 

class UsersDAO(BaseDAO):
    model = Users