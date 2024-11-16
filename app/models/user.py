from pydantic import BaseModel


class UserIn(BaseModel):
    email: str
    password: str


class User(UserIn):
    id: int | None = None
