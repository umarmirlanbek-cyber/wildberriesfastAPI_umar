from fastapi import HTTPException, Depends, APIRouter
from my_site.database.db import SessionLocal
from my_site.database.models import ProductImage
from my_site.database.schema import ProductImageInputSchema, ProductImageOutSchema
from sqlalchemy.orm import Session
from typing import List


product_image_router = APIRouter(prefix='/product-image',tags=['Product_image'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_image_router.post(path='/', response_model=ProductImageOutSchema)
async def create_product_image(product_image: ProductImageInputSchema, db: Session = Depends(get_db)):
    product_image_db = ProductImage(**product_image.dict())
    db.add(product_image_db)
    db.commit()
    db.refresh(product_image_db)
    return product_image_db

@product_image_router.get(path='/', response_model=List[ProductImageOutSchema])
async def list_product_image(db: Session = Depends(get_db)):
    return db.query(ProductImage).all()

@product_image_router.get(path='/{product_image_id}', response_model=ProductImageOutSchema)
async def detail_product_image(product_image_id: int, db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()
    if not product_image_db:
        raise HTTPException(status_code=404, detail='Мындай id жок')
    return product_image_db


@product_image_router.put('/{product_image_id}', response_model=dict)
async def update_product_image(product_image_id: int, product_image: ProductImageInputSchema,
                               db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()
    if not product_image_db:
        raise HTTPException(status_code=404, detail='Такого ID нет')

    for key, value in product_image.dict().items():
        setattr(product_image_db, key, value)

    db.commit()
    db.refresh(product_image_db)
    return {'message': 'Изображение Изменено'}


@product_image_router.delete('/{product_image_id}')
async def delete_product_image(product_image_id: int, db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id == product_image_id).first()
    if not product_image_db:
        raise HTTPException(status_code=404, detail='Такого ID нет')
    db.delete(product_image_db)
    db.commit()
    return {'message': 'Изображение Удалено'}