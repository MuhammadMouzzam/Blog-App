from typing import Tuple, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models
from . import Oauth2

router = APIRouter(tags=['Users'])

@router.post('/users/signup', response_model=schemas.UserOut)
def signUp(user: schemas.UserIn, db: Session = Depends(get_db)):
    user.password = Oauth2.hashing(user.password)
    user_in = models.User(**user.model_dump())
    db.add(user_in)
    db.commit()
    db.refresh(user_in)
    return user_in

@router.get("/users/{id}", response_model=Tuple[schemas.UserOut, List[schemas.BlogResponse]])
def find_user(id: int,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    blogs = db.query(models.Blogs).filter(models.Blogs.user_id == id).all()
    result = (user, blogs)
    return result

