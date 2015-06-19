from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, ForeignKey, Boolean
from flask.ext.login import UserMixin

from cakes.database import Base, engine, session


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(48), nullable=False, unique=True)
    products = relationship('Product', backref='brand')


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(48))
    color = Column(String(48))
    quantity = Column(Integer, default=int(1))
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    sub_category_id = Column(Integer, ForeignKey('sub_categories.id'))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    notes = Column(String(2048))
    favorite = Column(Boolean, default=True)

    def as_dictionary(self):
        product = {
            "id": self.id,
            "category_name": self.category.name,
            "brand_name": self.brand.name,
            "product_name": self.name,
            "product_color": self.color,
            "price": self.price,
            "notes": self.notes

        }
        return product


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True)
    sub_categories = relationship('SubCategory', backref='category')
    products = relationship('Product', backref='category')


class SubCategory(Base):
    __tablename__ = "sub_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    products = relationship('Product', backref='sub_category')


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    password = Column(String(128))


Base.metadata.create_all(engine)
