from collections import OrderedDict

from flask.ext.login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from app import db


class Brand(db.Model):
    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    products = db.relationship('Product', backref='brand')

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False,
                     info={'label': 'Product Name'})
    color = db.Column(db.String(128), info={'label': 'Color'})
    quantity = db.Column(db.Integer, default=int(1), info={'label': 'Quantity'})
    used = db.Column(db.Integer, default=int(0), info={'label': 'Used'})
    price = db.Column(db.Numeric(8, 2), info={'label': 'Price'})
    is_favorite = db.Column(db.Boolean, default=False,
                            info={'label': 'Favorite'})
    stars = db.Column(db.Float)
    review = db.Column(db.Text, info={'label': 'Review'})
    notes = db.Column(db.Text, info={'label': 'Notes'})

    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'))

    def as_dict(self):
        product = {
            "id": self.id,
            "brand_name": self.brand.name,
            "category": self.category.name,
            "subcategory": getattr(self.subcategory, 'name', None),
            "name": self.name,
            "color": self.color,
            "quantity": self.quantity,
            "used": self.used,
            "price": self.price,
            "is_favorite": self.is_favorite,
            "stars": self.stars,
            "review": self.review,
            "notes": self.notes
        }
        return product

    def _as_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    subcategories = db.relationship('Subcategory', backref='category')
    products = db.relationship('Product', backref='category')

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)


class Subcategory(db.Model):
    __tablename__ = "subcategories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    products = db.relationship('Product', backref='subcategory')

    def as_dict(self):
        subcategory = {
            "id": self.id,
            "name": self.name
        }
        return subcategory

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.username)

