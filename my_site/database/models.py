from typing import List, Optional
from datetime import date, datetime
from enum import Enum as PyEnum
from sqlalchemy import Integer, String, Date, Enum, ForeignKey, Text, Boolean, DateTime, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base


class Status_Choices(str, Enum):
    gold = 'gold'
    silver = 'silver'
    bronze = 'bronze'
    simple = 'simple'


class UserProfile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[str] = mapped_column(String)
    status: Mapped[Status_Choices] = mapped_column(PyEnum(Status_Choices), default=Status_Choices.simple)
    date_register: Mapped[date] = mapped_column(Date, default=date.today())

    user_review: Mapped[List['Review']] = relationship(back_populates='user',cascade='all, delete-orphan')
    refresh_users: Mapped[List['RefreshToken']] = relationship(back_populates='users',cascade='all, delete-orphan')

class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    users_id:Mapped[int] = mapped_column(ForeignKey('profile.id'))
    users: Mapped[UserProfile] = relationship(back_populates='refresh_users')
    token: Mapped[str] = mapped_column(String,nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)
    category_image: Mapped[str] = mapped_column(String)

    sub_category: Mapped[List['SubCategory']] = relationship(back_populates='category',
                                                             cascade='all, delete-orphan')


class SubCategory(Base):
    __tablename__ = 'subcategory'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subcategory_name: Mapped[str] = mapped_column(String(44), unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(back_populates='sub_category')

    product_sub: Mapped[List['Product']] = relationship(back_populates='subcategory',
                                                        cascade='all, delete-orphan')


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey('subcategory.id'))
    subcategory: Mapped[SubCategory] = relationship(back_populates='product_sub')
    product_type: Mapped[bool] = mapped_column(Boolean)
    article: Mapped[int] = mapped_column(Integer, unique=True)
    product_review: Mapped[List['Review']] = relationship(back_populates='products',
                                                          cascade='all, delete-orphan')

    product_photo: Mapped[List['ProductImage']] = relationship(back_populates='product')


class ProductImage(Base):
    __tablename__ = 'product_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped[Product] = relationship(back_populates='product_photo')

class Review(Base):

    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    user: Mapped[UserProfile] = relationship(back_populates='user_review')
    products_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    products: Mapped[Product] = relationship(back_populates='product_review')
    star: Mapped[int] = mapped_column(SmallInteger)
    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

