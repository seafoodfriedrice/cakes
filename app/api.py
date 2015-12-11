import json

from flask import Response

from cakes import app
from cakes.database import session
from cakes.models import Product


@app.route("/api/products", methods=["GET"])
def api_products():
    """ Return list of all products """

    products = session.query(Product).all()
    data = json.dumps([product.as_dictionary() for product in products])
    return Response(data, 200, mimetype="application/json")
