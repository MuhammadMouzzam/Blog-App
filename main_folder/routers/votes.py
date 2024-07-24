from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .Oauth2 import get_current_user
from ..schemas import VoteInfo
from ..database import get_db
from .. import models

router = APIRouter(tags=['Votes'])

@router.post('/votes/add')
def add_vote(vote_info: VoteInfo, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == vote_info.blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog Not Found')
    vote_query = db.query(models.Vote).filter(models.Vote.blog_id == vote_info.blog_id, models.Vote.user_id == current_user.id)
    vote = vote_query.first()
    if vote_info.dir == 0:
        if vote == None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vote Doesn't Exist")
        vote_query.delete()
        db.commit()
        return {'Message' : 'Vote Removed Successfully'}
    elif vote_info.dir == 1:
        if vote != None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vote Already Exists")
        vote_in = models.Vote(user_id=current_user.id, blog_id=vote_info.blog_id)
        db.add(vote_in)
        db.commit()
        db.refresh(vote_in)
        return {'Message' : 'Vote Added Successfully'}