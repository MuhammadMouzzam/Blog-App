from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..config import settings
from jose import jwt, JWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashing(password):
    return pwd_context.hash(password)

def verify_pass(user_pass, db_pass):
    return pwd_context.verify(user_pass, db_pass)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def generate_acces_token(data: dict):
    data_copy = data.copy()
    expire_time = datetime.utcnow() + timedelta(settings.access_token_expire_minutes)
    data_copy.update({'expire' : int(expire_time.timestamp())})
    token = jwt.encode(data_copy, settings.secret_key, algorithm=settings.algorithm)
    return token

def verify_access_token(token, cred_exception):
    try:
        payload = jwt.decode(token, key=settings.secret_key, algorithms=settings.algorithm)
        user_id = payload.get('user_id')
        expire_time = payload.get('expire')
        current_time = datetime.utcnow()
        if expire_time < int(current_time.timestamp()) or id is None:
            raise cred_exception
    except JWTError:
        cred_exception
    return user_id

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Individual Unauthorized')
    user_id = verify_access_token(token, cred_exception)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user
    