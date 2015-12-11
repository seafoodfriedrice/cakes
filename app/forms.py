from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import StringField, BooleanField, IntegerField
from wtforms import DecimalField, TextAreaField
from wtforms.validators import Required, Length, Optional

from app.database import session
from app.models import Category, Brand

def category_names():
    return session.query(Category).order_by(Category.name)

def brand_names():
    return session.query(Brand).order_by(Brand.name)

class ProductForm(Form):
    category = QuerySelectField(get_label='name', query_factory=category_names)
    brand = QuerySelectField(get_label='name', query_factory=brand_names)
    name = StringField(u'Product Name', validators=[Required()])
    color = StringField(u'Color', validators=[Length(max=48)])
    quantity = IntegerField(u'Quantity', default=1, validators=[Optional()])
    price = DecimalField(u'Price', default=0.0, validators=[Optional()])
    favorite = BooleanField(u'Favorite', default=False, validators=[Optional()])
    notes = TextAreaField(u'Product Notes', validators=[Optional()])
