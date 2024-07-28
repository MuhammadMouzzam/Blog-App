from datetime import datetime
from typing_extensions import TypedDict, List
from pydantic import BaseModel, EmailStr, conint

class Blog(BaseModel):
    tag : str
    content: str

class UserIn(BaseModel):
    email : EmailStr
    username : str
    password : str

class UserOut(BaseModel):
    username : str
    id : int
    created_at : datetime

class UserInfoOut(BaseModel):
    username : str
    id : int

class BlogResponse(BaseModel):
    tag : str
    content : str
    id : int
    owner : UserInfoOut
    created_at : datetime
    class config:
        orm_mode = True

class AccessToken(BaseModel):
    access_token : str
    token_type : str = 'Bearer'

class CommentIn(BaseModel):
    blog_id : int
    content : str

class CommentOut(BaseModel):
    id : int
    content : str
    owner : UserInfoOut
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

class CheckAdDict(TypedDict):
    User : UserInfoOut
    Blogs : List[CheckerAd]