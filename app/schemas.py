from typing import List, Optional
from pydantic import BaseModel


class Blog(BaseModel):
  title: str
  body: str
  user_id: int

  class Config():
    orm_mode = True


class BasicBlogInfo(BaseModel):
  id: int
  title: str
  body: str

  class Config():
    orm_mode = True


class User(BaseModel):
  name: str
  email: str
  password: str


class SimpleUserInfo(BaseModel):
  name: str
  email: str

  class Config():
    orm_mode = True


class ShowUser(BaseModel):
  name: str
  email: str
  blogs: List[BasicBlogInfo]

  class Config():
    orm_mode = True


class ShowBlog(BaseModel):
  id: int
  title: str
  body: str
  author: SimpleUserInfo

  class Config():
    orm_mode = True


class Login(BaseModel):
  username: str
  password: str


class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  email: Optional[str] = None