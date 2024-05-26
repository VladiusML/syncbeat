from typing import Optional
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_cache.decorator import cache

from musicdrop.likes.dao import LikeDAO
from musicdrop.users.dependencies import get_current_user, get_optional_current_user
from musicdrop.users.models import Users

router = APIRouter(
    prefix = "/pages",
    tags = ["Фронтенд"]
)

clients = []
templates = Jinja2Templates(directory="musicdrop/templates")

@router.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request, current_user: Optional[Users] = Depends(get_optional_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": current_user})

@router.get("/profile", response_class=HTMLResponse)
async def get_profile(request: Request, current_user: Users = Depends(get_current_user)):
    return templates.TemplateResponse("profile.html", {"request": request, "user": current_user})

