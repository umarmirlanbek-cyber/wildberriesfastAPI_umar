from fastapi import HTTPException, Depends, APIRouter
from my_site.database.db import SessionLocal
from my_site.database.models import UserProfile
from my_site.database.schema import UserProfileInputSchema, UserProfileOutSchema
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter(prefix='/user',tags=['User'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post(path='/', response_model=UserProfileOutSchema)
async def create_user(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = UserProfile(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.get(path='/', response_model=List[UserProfileOutSchema])
async def list_user(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()

@user_router.get(path='/{user_id}', response_model=UserProfileOutSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='Мындай id жок')
    return user_db


@user_router.put('/{user_id}', response_model=dict)
async def update_user(user_id: int, user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='Такого ID нет')

    for key, value in user.dict().items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)
    return {'message': 'Пользователь Изменён'}


@user_router.delete('/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='Такого ID нет')
    db.delete(user_db)
    db.commit()
    return {'message': 'Пользователь Удалён'}