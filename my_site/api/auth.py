from fastapi import HTTPException,Depends,APIRouter
from passlib.context import CryptContext
from my_site.database.db import SessionLocal
from my_site.database.models import UserProfile,RefreshToken
from my_site.database.schema import UserProfileInputSchema,UserProfileLoginSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta,datetime
from typing import Optional
from jose import jwt
from my_site.config import ALGORITHM,ACCESS_TOKEN_LIFETIME,REFRESH_TOKEN_LIFETIME,SECRET_KEY

auth_router = APIRouter(prefix='/auth',tags=['Auth'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(password,hashed_password):
    return pwd_context.verify(password,hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data:dict):
    return create_access_token(data,expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))



@auth_router.post('/register')
async def login(user:UserProfileInputSchema,db:Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if user_db or email_db:
        raise HTTPException(detail='Мындай username же email бар экен',status_code=400)
    new_password = get_password_hash(user.password)
    user_db = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        age=user.age,
        phone_number=user.phone_number,
        status=user.status,
        password=new_password
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@auth_router.post('/login')
async def login(user: UserProfileLoginSchema, db: Session = Depends(get_db)):
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if not email_db or not verify_password(user.password, email_db.password):
        raise HTTPException(detail='Неверные данные', status_code=400)
    access_token = create_access_token({'sub': email_db.email})
    refresh_token = create_refresh_token({'sub': email_db.email})
    refresh_db = RefreshToken(users_id=email_db.id,token=refresh_token)
    db.add(refresh_db)
    db.commit()
    return {'token_type': 'bearer','access_token':access_token, 'refresh_token':refresh_token}

@auth_router.post('/logout')
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stoped_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stoped_token:
        raise HTTPException(detail='Refresh token туура эмес', status_code=400)
    db.delete(stoped_token)
    db.commit()
    return {'message': 'Сайттан чыктыныз'}