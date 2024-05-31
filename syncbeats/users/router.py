from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse 
from exceptions import UserAlreadyExistsException, IncorrectUsernameOrPasswordException
from syncbeats.users.auth import create_access_token, get_password_hash, authenticate_user
from syncbeats.users.dependencies import get_current_user
from syncbeats.users.models import Users
from syncbeats.users.dao import UsersDAO
from fastapi.templating import Jinja2Templates

from syncbeats.users.schemas import SUserAuth, SUserLogin

templates = Jinja2Templates(directory="syncbeats/templates")

router = APIRouter(
    prefix = "/auth",
    tags=["Auth & Пользователи"]
)

@router.post("/register")
async def register_user(request: Request, user_data: SUserAuth):
    existing_user_email = await UsersDAO.find_one_or_none(email=user_data.email)
    existing_user_username = await UsersDAO.find_one_or_none(username=user_data.username)
    if existing_user_email or existing_user_username:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Пользователь с таким именем или электронной почтой уже существует"
        })

    try:
        hashed_password = get_password_hash(user_data.password)
        await UsersDAO.add(username=user_data.username, email=user_data.email, hashed_password=hashed_password)
    except ValueError as e:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": str(e)
        })

    return templates.TemplateResponse("login.html", {"request": request, "message": "Регистрация прошла успешно. Войдите в систему."})

@router.post("/login")
async def login_user(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    user = await authenticate_user(username, password)
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Неправильное имя пользователя или пароль"
        })
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("musicdrop_access_token", access_token, httponly=True)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/logout")
async def logout_user(response: Response):
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("musicdrop_access_token", httponly=True)
    return response

 