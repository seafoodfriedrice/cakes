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

@app.route("/product/add", methods=["GET", "POST"])
def product_add():
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()

    if request.method == "GET":
        return render_template("product_add.html", brands=brands,
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

        product.notes = Notes(text=request.form["notes"])

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

@app.route("/product/edit/<int:id>", methods=["GET", "POST"])
def product_edit(id):
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()
    product = session.query(Product).get(id)

    if request.method == "POST":
        product.name = request.form["product-name"].strip()
        product.color = request.form["color"].strip().title()
        product.price = float(request.form["price"].strip())
        product.notes.text=request.form["notes"]

        category = session.query(Category).filter_by(
            name=request.form["category"]).first()
        category.products.append(product)

        brand = session.query(Brand).filter_by(
            name=request.form["brand"]).first()
        brand.products.append(product)

        session.add_all([category, brand, product])

        try:
            session.commit()
            message = "{}Yay!{} {}{}{} has been updated.".format(
                "<strong>", "</strong>", "<em>", product.name, "</em>")
            flash(message, "success")
        except:
            session.rollback()
            message = "{}Uh-oh!{} Problem editing {}{}{}.".format(
                "<strong>", "</strong>", "<em>", product.name, "</em>")
            flash(error, "danger")

        return redirect(url_for("product_edit", id=product.id))
    else:
        return render_template("product_edit.html", brands=brands,
                               product=product, categories=categories)


@app.route("/products/brands/<int:id>")
def brand(id):
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()
    brand = session.query(Brand).get(id)

    if request.method == "GET":
        return render_template("brand.html", brands=brands, brand=brand,
                               categories=categories)

@app.route("/brand/add", methods=["GET", "POST"])
def brand_add():
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()

    if request.method == "POST":
        brand = Brand(name=request.form["brand-name"].strip())
        session.add(brand)

        try:
            session.commit()
            message = "{}More!{} Added {}{}{} to your Brands.".format(
                "<strong>", "</strong>", "<em>", brand.name, "</em>")
            flash(message, "success")
        except:
            session.rollback()
            message = "{}Oh no!{} Could not add {}{}{} to your Brands.".format(
                "<strong>", "</strong>", "<em>", brand.name, "</em>")
            flash(message, "danger")

        return redirect(url_for("products"))

    return render_template("brand_add.html", brands=brands, categories=categories)

@app.route("/products/categories/<int:id>")
def category(id):
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()
    category = session.query(Category).get(id)

    if request.method == "GET":
        return render_template("category.html", brands=brands, category=category,
                               categories=categories)
