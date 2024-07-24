from typing import List, Optional, Tuple
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from .Oauth2 import get_current_user
from ..database import get_db
from .. import models, schemas

router = APIRouter(tags=["Blogs"])

@router.get("/blogs", response_model=List[schemas.CheckerAd])
def get_all_blogs(db: Session = Depends(get_db), tag: Optional[str] = ''):
    blogs = db.query(models.Blogs, func.count(models.Vote.blog_id).label('votes')).join(models.Vote, onclause=models.Vote.blog_id == models.Blogs.id, isouter=True).group_by(models.Blogs.id).filter(models.Blogs.tag.contains(tag)).all()
    print(blogs)
    blogs = list(map(lambda x : x._mapping, blogs))
    print(blogs)
    blogs_list = []
    for blog in blogs:
        comments = db.query(models.Comment).filter(models.Comment.blog_id == blog['Blogs'].id).all()
        blogs_dict = {}
        blogs_dict.update({'Blog' : blog['Blogs'], 'Votes' : blog['votes'], 'Comments' : comments})
        blogs_list.append(blogs_dict)
    return blogs_list

@router.get('/blogs/{id}', response_model=schemas.CheckerAd)
def find_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs, func.count(models.Vote.blog_id).label('votes')).join(models.Vote, onclause=models.Vote.blog_id == models.Blogs.id, isouter=True).group_by(models.Blogs.id).filter(models.Blogs.id == int(id)).all()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog Not Found')
    blog = list(map(lambda x : x._mapping, blog))
    blog = blog[0]
    comments = db.query(models.Comment).filter(models.Comment.blog_id == int(id)).all()
    blog_dict = {'Blog' : blog['Blogs'], 'Votes' : blog['votes'], 'Comments' : comments}
    return blog_dict

@router.post("/blogs/add", response_model=schemas.BlogResponse)
def add_blog(blog: schemas.Blog, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    add_blog = models.Blogs(user_id=current_user.id ,**blog.model_dump())
    db.add(add_blog)
    db.commit()
    db.refresh(add_blog)
    return add_blog

@router.delete('/blogs/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == int(id))
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog Not Found')
    if blog.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Blog doesn't belong to this user")
    blog.delete()
    db.commit()

@router.put('/blogs/update/{id}', response_model=Tuple[schemas.BlogResponse, List[schemas.CommentOut]])
def update_blog(blog: schemas.Blog, id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    blog_query = db.query(models.Blogs).filter(models.Blogs.id == int(id))
    new_blog = blog_query.first()
    if not new_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog Not Found')
    if new_blog.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Blog doesn't belong to this user")
    blog_query.update(blog.model_dump())
    db.commit()
    db.refresh(new_blog)
    comments = db.query(models.Comment).filter(models.Comment.blog_id == int(id)).all()
    result = (new_blog, comments)
    return result