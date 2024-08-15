from typing import Tuple, List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models
from . import Oauth2

router = APIRouter(tags=['Users'])


@router.get("/users/{username}", response_model=schemas.CheckAdDict)
def find_user(username : str,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    blogs = db.query(models.Blogs, func.count(models.Vote.blog_id).label('votes')).join(models.Vote, onclause=models.Vote.blog_id == models.Blogs.id, isouter=True).group_by(models.Blogs.id).filter(models.Blogs.user_id == user.id).all()
    blogs = list(map(lambda x : x._mapping, blogs))
    blogs_list = []
    for blog in blogs:
        comments = db.query(models.Comment).filter(models.Comment.blog_id == blog['Blogs'].id).all()
        blogs_dict = {}
        blogs_dict.update({'Blog' : blog['Blogs'], 'Votes' : blog['votes'], 'Comments' : comments})
        blogs_list.append(blogs_dict)
    result = {'User' : user, 'Blogs' : blogs_list}
    return result

