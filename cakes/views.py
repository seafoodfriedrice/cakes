import re
from datetime import datetime

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import exc

from cakes import app
from cakes.database import session
from cakes.models import Brand, Category, SubCategory, Product, Notes


@app.route("/")
@app.route("/products")
def products():
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()

    products = session.query(Product).order_by(Product.id.desc()).all()
    return render_template("products.html", brands=brands, products=products,
                           categories=categories)

@app.route("/products/add", methods=["GET", "POST"])
def products_add():
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()

    if request.method == "GET":
        return render_template("products_add.html", brands=brands,
                               categories=categories)

    if request.method == "POST":
        brand = session.query(Brand).filter_by(
            name=request.form["brand"]).first()
        category = session.query(Category).filter_by(
            name=request.form["category"]).first()

        product_name = request.form["product-name"].strip().title()
        product = Product(name=product_name)
        product.color = request.form["color"].strip()

        # Remove dollar sign from price
        product.price = re.sub('\$', '', request.form["price"].strip())

        brand.products.append(product)
        category.products.append(product)

        session.add_all([brand, category, product])

        try:
            session.commit()
            message = "{}Mine!{} Added {}{}{} to your collection.".format(
                "<strong>", "</strong>", "<em>", product_name, "</em>")
            flash(message, "success")
        except:
            session.rollback()
            message = "{}Uh-oh!{} Could not add {}{}{}.".format(
                "<strong>", "</strong>", "<em>", product_name, "</em>")
            flash(error, "danger")

        return redirect(url_for("products", brands=brands,
                               products=products, categories=categories))
