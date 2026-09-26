from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth.security import create_access_token,hash_password,verify_password
from app.database.session import get_db
from app.models import User
from app.schemas import Token,UserCreate,UserOut
router=APIRouter(prefix='/auth',tags=['auth'])
@router.post('/register',response_model=UserOut,status_code=201)
def register(payload:UserCreate,db:Session=Depends(get_db)):
 if db.query(User).filter(User.email==payload.email).first(): raise HTTPException(409,'Email already registered')
 u=User(email=payload.email,hashed_password=hash_password(payload.password),full_name=payload.full_name,role=payload.role);db.add(u);db.commit();db.refresh(u);return u
@router.post('/login',response_model=Token)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
 u=db.query(User).filter(User.email==form_data.username).first()
 if not u or not verify_password(form_data.password,u.hashed_password): raise HTTPException(status_code=401,detail='Invalid credentials')
 return Token(access_token=create_access_token(u.id))
