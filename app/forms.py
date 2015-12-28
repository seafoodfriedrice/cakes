from flask import flash
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import StringField
from wtforms.validators import Optional
from wtforms_alchemy import ModelForm, model_form_factory
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
    category = QuerySelectField(query_factory=category_names)
    sub_categories = StringField(u'New Subcategory')
    sub_category = QuerySelectField(
        get_label='name',
        query_factory=sub_category_names,
        allow_blank=True
    )


class ProductForm(ModelForm):
    class Meta:
        model = Product

    brand = QuerySelectField(query_factory=brand_names)
    category = QuerySelectField(query_factory=category_names)
    sub_category = QuerySelectField(query_factory=sub_category_names)
