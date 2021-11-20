from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime

from pydantic.types import conint


class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode = True

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner:UserResponse

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class User(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class Tokendata(BaseModel):
    id:Optional[str]=None


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
    