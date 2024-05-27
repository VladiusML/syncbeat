from sqladmin import ModelView
from syncbeats.users.models import Users

class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.username, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon  = "fa-solid fa-user"

