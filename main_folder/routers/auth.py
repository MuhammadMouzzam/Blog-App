from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from . import Oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.AccessToken)
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(user_creds.username)
    db_user = db.query(models.User).filter(models.User.email == user_creds.username).first()
    print(db_user)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    pass_check = Oauth2.verify_pass(user_pass=user_creds.password, db_pass=db_user.password)
    if not pass_check:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    access_token = Oauth2.generate_acces_token({'user_id' : db_user.id})
    token = schemas.AccessToken(access_token=access_token)
    return token