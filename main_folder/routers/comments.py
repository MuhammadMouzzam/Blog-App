from typing import List, Tuple
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .Oauth2 import get_current_user


router = APIRouter(tags=['Comments'])

@router.post('/comments/add', response_model=Tuple[schemas.BlogResponse, List[schemas.CommentOut]])
def add_comment(comment: schemas.CommentIn, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_comment = models.Comment(user_id=current_user.id, **comment.model_dump())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    blog = db.query(models.Blogs).filter(models.Blogs.id == comment.blog_id).first()
    comments = db.query(models.Comment).filter(models.Comment.blog_id == comment.blog_id).all()
    result = (blog, comments)
    return result

@router.delete('/comments/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    comment = db.query(models.Comment).filter((models.Comment.id == id))
    if not comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment Not Found')
    blog = db.query(models.Blogs).filter(models.Blogs.id == comment.first().blog_id).first()
    if comment.first().user_id != current_user.id or current_user.id != blog.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to delete this comment")
    comment.delete()
    db.commit()

@router.put('/comments/update/{id}', response_model=Tuple[schemas.BlogResponse, List[schemas.CommentOut]])
def update_comment(id: int, comment_info: schemas.CommentInfo, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    comment_query = db.query(models.Comment).filter((models.Comment.id == id))
    comment = comment_query.first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment Not Found')
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to update this comment")
    comment_query.update(comment_info.model_dump())
    db.commit()
    db.refresh(comment)
    blog = db.query(models.Blogs).filter(models.Blogs.id == comment.blog_id).first()
    comments = db.query(models.Comment).filter(models.Comment.blog_id == comment.blog_id).all()
    result = (blog, comments)
    return result

