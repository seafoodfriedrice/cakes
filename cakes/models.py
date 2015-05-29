from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, ForeignKey

from cakes.database import Base, engine


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(24), nullable=False, unique=True)
    items = relationship('Item', backref='brand')


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    sub_category_id = Column(Integer, ForeignKey('sub_categories.id'))
    brand_id = Column(Integer, ForeignKey('brands.id'))
    notes = relationship('Notes', backref='item')


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True)
    sub_categories = relationship('SubCategory', backref='category')
    items = relationship('Item', backref='category')


class SubCategory(Base):
    __tablename__ = "sub_categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    items = relationship('Item', backref='sub_category')


class Notes(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True)
    text = Column(String(256))
    item_id = Column(Integer, ForeignKey('items.id'))


Base.metadata.create_all(engine)
