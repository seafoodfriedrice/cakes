import json

from flask import Response

from app import app, db
from app.database import session
from app.models import Product, Category, SubCategory


@app.route("/api/products", methods=["GET"])
def api_products():
    """ Return list of all products """

    products = Product.query.all()
    data = json.dumps([product.as_dict() for product in products])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/categories/<int:id>/subcategories", methods=["GET"])
def api_subcategories(id):
    """ Return list of subcategories by category.id """

    sub_categories = SubCategory.query.join(Category).filter(
        Category.id == id
    ).all()
    data = json.dumps([sub_category.as_dict()
                       for sub_category in sub_categories])
    return Response(data, 200, mimetype="application/json")
