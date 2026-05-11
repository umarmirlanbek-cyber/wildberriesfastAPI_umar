from fastapi import HTTPException, Depends, APIRouter
from my_site.database.db import SessionLocal
from my_site.database.models import Product
from my_site.database.schema import ProductInputSchema, ProductOutSchema
from sqlalchemy.orm import Session
from typing import List


product_router = APIRouter(prefix='/product',tags=['Product'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_router.post(path='/', response_model=ProductOutSchema)
async def create_product(product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db

@product_router.get(path='/', response_model=List[ProductOutSchema])
async def list_product(db: Session = Depends(get_db)):
    return db.query(Product).all()

@product_router.get(path='/{product_id}', response_model=ProductOutSchema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Мындай id жок')
    return product_db


@product_router.put('/{product_id}', response_model=dict)
async def update_product(product_id: int, product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Такого ID нет')

    for key, value in product.dict().items():
        setattr(product_db, key, value)

    db.commit()
    db.refresh(product_db)
    return {'message': 'Продукт Изменён'}


@product_router.delete('/{product_id}')
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Такого ID нет')
    db.delete(product_db)
    db.commit()
    return {'message': 'Продукт Удалён'}