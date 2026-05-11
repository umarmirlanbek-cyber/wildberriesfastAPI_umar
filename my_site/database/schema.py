from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from .models import Status_Choices


class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    age: Optional[int]
    phone_number: str
    status: Status_Choices
    date_register: date


class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    age: Optional[int]
    phone_number: str
    status: Status_Choices

class UserProfileLoginSchema(BaseModel):
    email: EmailStr
    password: str


class CategoryOutSchema(BaseModel):
    id: int
    category_name: str
    category_image: str


class CategoryInputSchema(BaseModel):
    category_name: str
    category_image: str


class SubCategoryOutSchema(BaseModel):
    id: int
    subcategory_name: str
    category_id: int


class SubCategoryInputSchema(BaseModel):
    subcategory_name: str
    category_id: int


class ProductOutSchema(BaseModel):
    id: int
    product_name: str
    price: int
    description: str
    subcategory_id: int
    product_type: bool
    article: int


class ProductInputSchema(BaseModel):
    product_name: str
    price: int
    description: str
    subcategory_id: int
    product_type: bool
    article: int


class ProductImageOutSchema(BaseModel):
    id: int
    product_id: int
    product_image: str


class ProductImageInputSchema(BaseModel):
    product_id: int
    product_image: str


class ReviewOutSchema(BaseModel):
    id: int
    user_id: int
    products_id: int
    star: int
    text: str
    created_date: datetime


class ReviewInputSchema(BaseModel):
    user_id: int
    products_id: int
    star: int
    text: str