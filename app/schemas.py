from typing import Literal
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass


# TODO
class PostUpdate(BaseModel):
    title: str = None
    content: str = None
    is_published: bool = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse

    class Config:
        orm_mode = True


class PostVote(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None


class VoteAction(BaseModel):
    post_id: int
    direction: Literal[0, 1]
