from fastapi import HTTPException, Depends, APIRouter
from my_site.database.db import SessionLocal
from my_site.database.models import SubCategory
from my_site.database.schema import SubCategoryInputSchema, SubCategoryOutSchema
from sqlalchemy.orm import Session
from typing import List

subcategory_router = APIRouter(prefix='/subcategory',tags=['SubCategory'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@subcategory_router.post(path='/', response_model=SubCategoryOutSchema)
async def create_subcategory(subcategory: SubCategoryInputSchema, db: Session = Depends(get_db)):
    subcategory_db = SubCategory(**subcategory.dict())
    db.add(subcategory_db)
    db.commit()
    db.refresh(subcategory_db)
    return subcategory_db

@subcategory_router.get(path='/', response_model=List[SubCategoryOutSchema])
async def list_subcategory(db: Session = Depends(get_db)):
    return db.query(SubCategory).all()

@subcategory_router.get(path='/{subcategory_id}', response_model=SubCategoryOutSchema)
async def detail_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory_db:
        raise HTTPException(status_code=404, detail='Мындай id жок')
    return subcategory_db


@subcategory_router.put('/{subcategory_id}', response_model=dict)
async def update_subcategory(subcategory_id: int, subcategory: SubCategoryInputSchema, db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory_db:
        raise HTTPException(status_code=404, detail='Такого ID нет')

    for key, value in subcategory.dict().items():
        setattr(subcategory_db, key, value)

    db.commit()
    db.refresh(subcategory_db)
    return {'message': 'Подкатегория Изменена'}


@subcategory_router.delete('/{subcategory_id}')
async def delete_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory_db:
        raise HTTPException(status_code=404, detail='Такого ID нет')
    db.delete(subcategory_db)
    db.commit()
    return {'message': 'Подкатегория Удалена'}