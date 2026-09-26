from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.auth.security import InvalidTokenError,decode_access_token
from app.database.session import get_db
from app.models import User,UserRole
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='/auth/login')
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
 try: uid=decode_access_token(token)
 except InvalidTokenError: raise HTTPException(status_code=401,detail='Invalid or expired token')
 user=db.get(User,uid)
 if not user or not user.is_active: raise HTTPException(status_code=401,detail='Inactive or missing user')
 return user
def require_role(*roles):
 def dep(user:User=Depends(get_current_user)):
  if user.role not in roles: raise HTTPException(status_code=403,detail='Insufficient permissions')
  return user
 return dep
