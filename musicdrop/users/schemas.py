from pydantic import BaseModel, EmailStr
from datetime import date 

class SUserAuth(BaseModel):

    username: str
    email: EmailStr
    password: str

class SUserLogin(BaseModel):

    username: str
    password: str

 