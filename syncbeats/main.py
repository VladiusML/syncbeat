from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
 
from syncbeats.config import settings
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqladmin import Admin, ModelView

from syncbeats.admin.views import UserAdmin
from syncbeats.database import engine
from syncbeats.users.models import Users

from syncbeats.users.router import router as router_users
from syncbeats.pages.router import router as router_pages 
from syncbeats.likes.router import router as router_likes
from syncbeats.admin.auth import authentication_backend

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis


origins = [
    "http://host:8000"
]

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="syncbeats/static"), "static")


app.include_router(router_users)
app.include_router(router_pages)

app.include_router(router_likes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers = ["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin"
                     "Authorization"]
)


#admin = Admin(app, engine, authentication_backend=authentication_backend)
#admin.add_view(UserAdmin)