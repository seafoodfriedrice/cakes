from flask.ext.login import UserMixin
from app import db


class Brand(db.Model):
    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    products = db.relationship('Product', backref='brand')

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "<Brand {!r}>".format(self.name)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), info={'label': 'Product Name'})
    color = db.Column(db.String(64), info={'label': 'Color'})
    quantity = db.Column(db.Integer, default=int(1), info={'label': 'Quantity'})
    price = db.Column(db.Float, info={'label': 'Price'})
    favorite = db.Column(db.Boolean, default=False, info={'label': 'Favorite'})
    stars = db.Column(db.Float)
    review = db.Column(db.Text, info={'label': 'Review'})
    notes = db.Column(db.Text, info={'label': 'Notes'})
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    sub_category_id = db.Column(db.Integer, db.ForeignKey('sub_categories.id'))

    def as_dict(self):
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

    def __repr__(self):
        return "<Product {!r}>".format(self.name)


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    sub_categories = db.relationship('SubCategory', backref='category')
    products = db.relationship('Product', backref='category')

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "<Category {!r}>".format(self.name)


class SubCategory(db.Model):
    __tablename__ = "sub_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    products = db.relationship('Product', backref='sub_category')

    def as_dict(self):
        sub_category = {
            "id": self.id,
            "name": self.name
        }
        return sub_category

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "<SubCategory {!r}>".format(self.name)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return "<User {!r}>".format(self.username)

