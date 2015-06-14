from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField
from wtforms import DecimalField, SelectField, TextAreaField
from wtforms.validators import Required, Length, Optional

from cakes.database import session


class ProductForm(Form):
    category = SelectField(u'Category', coerce=int, validators=[Required()])
    brand = SelectField(u'Brand', coerce=int, validators=[Required()])
    name = StringField(u'Product Name', validators=[Required()])
    color = StringField(u'Color', validators=[Length(max=48)])
    quantity = IntegerField(u'Quantity', default=1, validators=[Optional()])
    price = DecimalField(u'Price', default=0.0, validators=[Optional()])
    favorite = BooleanField(u'Favorite', default=False, validators=[Optional()])
    notes = TextAreaField(u'Product Notes', validators=[Optional()])
