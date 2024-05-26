from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from exceptions import IncorrectUsernameOrPasswordException
from musicdrop.users.auth import authenticate_user, create_access_token
from musicdrop.users.dependencies import get_current_user
from musicdrop.config import settings

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        user = await authenticate_user(username, password)
        if user:
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        
        user = await get_current_user(token)
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        return True
         


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)