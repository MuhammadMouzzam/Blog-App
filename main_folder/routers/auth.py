from fastapi import APIRouter, Depends, Request, HTTPException, status
from authlib.integrations.starlette_client import OAuth, OAuthError
from sqlalchemy.orm import Session
from ..database import get_db
from ..config import settings
from .. import models, schemas
from . import Oauth2

router = APIRouter(tags=['Authentication'])
oauth = OAuth()
oauth.register(
    name = 'google',
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    client_id = settings.client_id,
    client_secret = settings.client_secret,
    client_kwargs = {
        'scope' : 'email openid profile',
        'redirect_url' : 'https://blog-app-t73e.onrender.com/login/redirect'
    }
)

@router.get('/login')
async def login(request : Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)

@router.get('/login/redirect') #, response_model=schemas.AccessToken
async def auth(request : Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Authentication Failed')
    user = token.get('userinfo')
    if user:
        request.session['user'] = user
    db_user = db.query(models.User).filter(models.User.username == user['name']).first()
    if not db_user:
        db_user = models.User(email=user['email'], username=Oauth2.remove_spaces(user['name']))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    access_token = Oauth2.generate_acces_token({'user_id' : db_user.id})
    token = schemas.AccessToken(access_token=access_token)
    return token