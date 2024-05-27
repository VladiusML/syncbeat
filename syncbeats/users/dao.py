from syncbeats.database import async_session_maker
from syncbeats.dao.base import BaseDAO
from syncbeats.users.models import Users

from sqlalchemy import select 

class UsersDAO(BaseDAO):
    model = Users