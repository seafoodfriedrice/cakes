from flask import flash
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import StringField, BooleanField, IntegerField
from wtforms import DecimalField, TextAreaField, FormField, FieldList
from wtforms.validators import Required, Length, Optional
from wtforms_alchemy import ModelForm, ModelFieldList, model_form_factory,\
                            ModelFormField
from wtforms.fields import FormField

from app import db
from app.models import Brand, Category, SubCategory, Product

''' http://flask.pocoo.org/snippets/12/ '''
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error)
            )

# Required to use WTForms-Alchemy with Flask-WTF
BaseModelForm = model_form_factory(Form, strip_string_fields=True)
class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

# SQLAlchemy query objects used by QuerySelectField()
def brand_names():
    return Brand.query.order_by(Brand.name)
def category_names():
    return Category.query.order_by(Category.name)
def sub_category_names():
    return SubCategory.query.order_by(SubCategory.name)

'''
class ProductForm(Form):
    brand = QuerySelectField(get_label='name', query_factory=brand_names)
    category = QuerySelectField(get_label='name', query_factory=category_names)
    sub_category = QuerySelectField(get_label='name',
        query_factory=sub_category_names)
    name = StringField(u'Product Name', validators=[Required()])
    color = StringField(u'Color', validators=[Length(max=48)])
    quantity = IntegerField(u'Quantity', default=1, validators=[Optional()])
    price = DecimalField(u'Price', validators=[Optional()])
    favorite = BooleanField(u'Favorite', default=False, validators=[Optional()])
    stars = DecimalField(u'Stars', validators=[Optional()])
    review = TextAreaField(u'Review', validators=[Optional()])
    notes = TextAreaField(u'Notes', validators=[Optional()])
'''
class BrandForm(ModelForm):
    class Meta:
        model = Brand

class SubCategoryForm(ModelForm):
    class Meta:
        model = SubCategory


class CategoryForm(ModelForm):
    class Meta:
        model = Category

    name = StringField(validators=[Optional()])
    sub_categories = StringField(u'New Subcategory')
    sub_category = QuerySelectField(get_label='name',
        query_factory=sub_category_names, allow_blank=True)
    

class ProductForm(ModelForm):
    class Meta:
        model = Product

    brand = QuerySelectField(query_factory=brand_names)
    category = QuerySelectField(query_factory=category_names)
    sub_category = QuerySelectField(query_factory=sub_category_names)

'''
class CategoryForm(Form):
    name = StringField(u'New Category', validators=[Length(max=64)])
    sub_category = QuerySelectField(get_label='name',
        query_factory=sub_category_names, allow_blank=True)
    sub_categories = StringField(u'New Subcategory')
'''

'''
class SubCategoryForm(Form):
    name = StringField(u'Subcategory Name',
                       validators=[Required(), Length(max=64)])
    category = QuerySelectField(get_label='name', query_factory=category_names)
    '''
