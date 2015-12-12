from flask.ext.login import UserMixin
from app import db


class Brand(db.Model):
    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    products = db.relationship('Product', backref='brand')


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    color = db.Column(db.String(64))
    quantity = db.Column(db.Integer, default=int(1))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    sub_category_id = db.Column(db.Integer, db.ForeignKey('sub_categories.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    notes = db.Column(db.Text))
    favorite = db.Column(db.Boolean, default=True)

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


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    sub_categories = db.relationship('SubCategory', backref='category')
    products = db.relationship('Product', backref='category')


class SubCategory(db.Model):
    __tablename__ = "sub_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    products = db.relationship('Product', backref='sub_category')


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))
