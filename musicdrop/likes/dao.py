from musicdrop.database import async_session_maker
from musicdrop.likes.models import Like
from sqlalchemy import func, select, update
from musicdrop.dao.base import BaseDAO

class LikeDAO(BaseDAO):
    model = Like

 
    @classmethod
    async def get_total_likes(cls):
        async with async_session_maker() as session:
            query = select(func.sum(Like.count))  # Используем функцию SUM для подсчета общего количества лайков
            result = await session.execute(query)
            total_likes = result.scalar_one_or_none()
            return total_likes

    @classmethod
    async def increment(cls, user_id):
        async with async_session_maker() as session:
            existing_like = await session.execute(select(cls.model).filter_by(user_id=user_id))
            like = existing_like.scalar_one_or_none()
            if like:
                # Если лайк уже существует, не увеличиваем счетчик
                return
            new_like = Like(user_id=user_id, count=1)
            session.add(new_like)
            await session.commit()

    