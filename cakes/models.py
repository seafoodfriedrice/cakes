from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, ForeignKey

from cakes.database import Base, engine


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(24), nullable=False, unique=True)
    products = relationship('Product', backref='brand')


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    sub_category_id = Column(Integer, ForeignKey('sub_categories.id'))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    notes = relationship('Notes', backref='Product')


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


class Notes(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True)
    text = Column(String(256))
    item_id = Column(Integer, ForeignKey('products.id'))


Base.metadata.create_all(engine)
