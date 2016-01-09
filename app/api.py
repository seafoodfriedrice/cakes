import pdb
import simplejson
from pprint import pprint

from flask import Response, jsonify, request, json
from wtforms_json import flatten_json

from app import app, db
from .forms import ProductForm
from .models import Product, Brand, Category, Subcategory


@app.route("/api/products", methods=["GET", "POST"])
def api_products():
    if request.method == "GET":
        products = Product.query.all()
        data = simplejson.dumps([product.as_dict() for product in products])
        return Response(data, 200, mimetype="application/json")
    if request.method == "POST":
        form = ProductForm.from_json(request.json)
        data = form.patch_data
        product = Product(**data)
        db.session.add(product)
        db.session.commit()
        return jsonify(request.json)

@app.route("/api/products/<int:id>", methods=["GET", "PUT"])
def api_product(id):
    product = Product.query.get_or_404(id)
    if request.method == "GET":
        return jsonify(product._as_dict())
    if request.method == "PUT":
        form = ProductForm.from_json(request.json)
        form.populate_obj(product)
        db.session.commit()
        return jsonify(request.json)

@app.route("/api/categories/<int:id>/subcategories", methods=["GET"])
def api_subcategories(id):
    """ Return list of subcategories by parent category.id """
    subcategories = (
        Subcategory.query.join(Category)
        .filter(Category.id == id)
        .all()
    )
    data = simplejson.dumps([subcategory.as_dict()
                             for subcategory in subcategories])
    return Response(data, 200, mimetype="application/json")
