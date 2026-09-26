from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from app.config.settings import settings
pwd=CryptContext(schemes=['bcrypt'],deprecated='auto')
class InvalidTokenError(Exception): pass
def hash_password(p): return pwd.hash(p)
def verify_password(p,h): return pwd.verify(p,h)
def create_access_token(subject): return jwt.encode({'sub':subject,'exp':datetime.now(timezone.utc)+timedelta(minutes=settings.jwt_expire_minutes)},settings.jwt_secret,algorithm=settings.jwt_algorithm)
def decode_access_token(token):
 try:
  data=jwt.decode(token,settings.jwt_secret,algorithms=[settings.jwt_algorithm]); sub=data.get('sub')
  if not sub: raise InvalidTokenError('Missing subject')
  return sub
 except JWTError as e: raise InvalidTokenError('Invalid token') from e
