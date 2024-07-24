from datetime import datetime
from typing import List, TypedDict
from pydantic import BaseModel, EmailStr, conint

class BlogResponse(BaseModel):
    tag : str
    content : str
    id : int
    created_at : datetime

class Blog(BaseModel):
    tag : str
    content: str

class UserIn(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    email : EmailStr
    id : int
    created_at : datetime

class AccessToken(BaseModel):
    access_token : str
    token_type : str = 'Bearer'

class CommentIn(BaseModel):
    blog_id : int
    content : str

class CommentOut(BaseModel):
    id : int
    content : str
    created_at : datetime

class CommentInfo(BaseModel):
    content : str

class VoteInfo(BaseModel):
    blog_id: int
    dir: conint(le=1) # type: ignore
    
class CheckerAd(TypedDict):
    Blog : BlogResponse
    Votes : int
    Comments : List[CommentOut]
