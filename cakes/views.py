from datetime import datetime

from flask import render_template, request, redirect, url_for, flash

from cakes import app
from cakes.database import session
from cakes.models import Brand, Category, SubCategory, Product, Notes


brands = session.query(Brand).order_by(Brand.name.asc()).all()
categories = session.query(Category).order_by(Category.name.asc()).all()

@app.route("/")
@app.route("/products")
def products():
    products = session.query(Product).all()
    return render_template("products.html", brands=brands, products=products,
                           categories=categories)

@app.route("/products/add")
def products_add():
    return render_template("products_add.html", brands=brands,
                           categories=categories)
