import wtforms_json

from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import StringField
from wtforms.validators import Optional
from wtforms_alchemy import ModelForm, model_form_factory

from app import db
from .models import Brand, Category, Subcategory, Product


wtforms_json.init()

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

def subcategory_names():
    return Subcategory.query.order_by(Subcategory.name)


class BrandForm(ModelForm):
    class Meta:
        model = Brand


class SubcategoryForm(ModelForm):
    class Meta:
        model = Subcategory


class CategoryForm(ModelForm):
    class Meta:
        model = Category

    new_category = StringField(validators=[Optional()])
    new_subcategory = StringField(u'New Subcategory')
    category = QuerySelectField(query_factory=category_names)
    subcategory = QuerySelectField(query_factory=subcategory_names,
                                   allow_blank=True)


class ProductForm(ModelForm):
    class Meta:
        model = Product

    brand = QuerySelectField(query_factory=brand_names, allow_blank=True)
    category = QuerySelectField(query_factory=category_names, allow_blank=True)
    subcategory = QuerySelectField(query_factory=subcategory_names,
                                   allow_blank=True)
