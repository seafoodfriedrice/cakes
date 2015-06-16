import re
from datetime import datetime

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import exc
from sqlalchemy import func

from cakes import app
from cakes.database import session
from cakes.models import Brand, Category, SubCategory, Product, Notes
from cakes.forms import ProductForm



@app.route("/")
@app.route("/products")
def products():
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()

    products = session.query(Product).order_by(Product.id.desc()).all()
    price_total = session.query(func.sum(Product.price).label(
        'product_price_total')).scalar()
    return render_template("products.html", brands=brands, products=products,
                           categories=categories, price_total=price_total)

def flash_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error), "danger")

@app.route("/product/test_add", methods=["GET", "POST"])
def test_add():
    form = ProductForm()

    if form.validate_on_submit():
        product = Product(name=form.name.data, note=form.notes.data)

        for field in ['category', 'brand', 'color', 'quantity',
                      'price', 'favorite']:
            setattr(product, field, getattr(form, field).data)

        session.add(product)
        session.commit()

        href_url_for = url_for("product_edit", id=product.id)
        message = "{}Mine!{} Added {} {} <a href='{}' class='alert-link'>{}</a> to your collection.".format(
            "<strong>", "</strong>", form.brand.data, product.name, href_url_for, product.color)
        flash(message, "success")

        if request.form["submit"] == "Add":
            return redirect(url_for("products"))
        # Redirect back to test_add() when
        # Add Another button is pressed
        else:
            # Clear out the color form so we can quickly add
            # products that are similar in category and brand
            form.color.data = None
            return render_template("test_add.html", form=form)
    else:
        flash_form_errors(form)

    return render_template("test_add.html", form=form)

@app.route("/product/test_edit/<int:id>", methods=["GET", "POST"])
def test_edit(id):
    product = session.query(Product).get(id)
    form = ProductForm(obj=product)
    # TODO: Need to refactor models.py to merge Notes into
    #       Product so we don't have to stuff like this
    #form.notes.data = product.notes.text

    if request.method == "POST" and form.validate_on_submit():
        product.notes.text = request.form["notes"]

        for field in ['category', 'brand', 'color', 'quantity',
                      'price', 'favorite']:
            setattr(product, field, getattr(form, field).data)

        session.add(product)
        session.commit()

        message = "{}Done!{} Edited {} {} {}{}{} successfully.".format(
            "<strong>", "</strong>", form.brand.data, product.name,
            '<a href="#" class="alert-link">', product.color, "</a>")
        flash(message, "success")

        if request.form["submit"] == "Add":
            return redirect(url_for("products"))
        # Redirect back to test_add() when
        # Add Another button is pressed
        else:
            # Clear out the color form so we can quickly add
            # products that are similar in category and brand
            form.color.data = None
            return render_template("test_add.html", form=form)
    else:
        flash_form_errors(form)

    return render_template("test_add.html", form=form)

@app.route("/product/add", methods=["GET", "POST"])
def product_add():
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()

    if request.method == "POST":
        brand = session.query(Brand).filter_by(
            name=request.form["brand"]).first()
        category = session.query(Category).filter_by(
            name=request.form["category"]).first()

        product_name = request.form["product-name"].strip().title()
        product = Product(name=product_name)

        if request.form["price"] != None:
            product.price = request.form["price"]

        product.quantity = request.form["quantity"]

        product.favorite = request.form.get("is-favorite", False)
        product.color = request.form.get("color", "").strip()
        product.notes = Notes()
        product.notes.text = request.form.get("notes")

        brand.products.append(product)
        category.products.append(product)

        session.add_all([brand, category, product])

        try:
            session.commit()
            message = "{}Mine!{} Added {} {} {}{}{} to your collection.".format(
                "<strong>", "</strong>", brand.name, product_name,
                "<em>", product.color, "</em>")
            flash(message, "success")
        except:
            session.rollback()
            message = "{}Uh-oh!{} Could not add {}{}{}.".format(
                "<strong>", "</strong>", "<em>", product_name, "</em>")
            flash(message, "danger")

        if request.form["submit"] == "Add":
            return redirect(url_for("products", brands=brands,
                                    products=products, categories=categories))
        # Redirect back to product_add() when Add Another button is pressed
        else:
            kwargs = {
                "category": category,
                "brand": brand,
                "product": product,
                "brands": brands,
                "categories": categories,

            }
            return render_template("product_add.html", **kwargs)

    else:
         return render_template("product_add.html", brands=brands,
                                     categories=categories)


@app.route("/product/edit/<int:id>", methods=["GET", "POST"])
def product_edit(id):
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()
    product = session.query(Product).get(id)

    if request.method == "POST":

        if request.form["submit"] == "Delete":
            session.delete(product)
            try:
                session.commit()
                message = "{}Bye-bye!{} {}{}{} removed from inventory.".format(
                    "<strong>", "</strong>", "<em>", product.name, "</em>")
                flash(message, "success")
            except:
                session.rollback()
                message = "{}Oh noes!{} Couldn't delete {}{}{}.".format(
                    "<strong>", "</strong>", "<em>", product.name, "</em>")
                flash(error, "danger")

            return redirect(url_for("products"))
            
        if request.form["submit"] == "Save":
            product.name = request.form["product-name"].strip()
            if request.form["color"]:
                product.color = request.form["color"].strip().title()
            if request.form["price"]:
                product.price = float(request.form["price"].strip())
            product.notes.text=request.form["notes"]

            product.favorite = request.form.get("is-favorite", False)
            product.quantity = request.form["quantity"]

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

            return redirect(url_for("products"))

    return render_template("product_edit.html", brands=brands,
                           product=product, categories=categories)



@app.route("/products/brands/<int:id>", methods=["GET", "POST"])
def brand(id):
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()
    brand = session.query(Brand).get(id)

    if request.method == "POST":
        brand.name = request.form["brand-name"].strip()
        session.add(brand)
        try:
            session.commit()
            message = "{}Makeover!{} Brand name changed to {}{}{}.".format(
                "<strong>", "</strong>", "<em>", brand.name, "</em>")
            flash(message, "success")
        except:
            session.rollback()
            message = "{}Whoops!{} Couldn't change name for {}{}{}.".format(
                "<strong>", "</strong>", "<em>", brand.name, "</em>")
            flash(message, "danger")
        return redirect(url_for("brand", id=brand.id,
                                products=products, categories=categories))

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



@app.route("/products/categories/<int:id>", methods=["GET", "POST"])
def category(id):
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()
    category = session.query(Category).get(id)

    if request.method == "POST":
        category.name = request.form["category-name"].strip()
        session.add(category)
        try:
            session.commit()
            message = "{}Makeover!{} Category name changed to {}{}{}.".format(
                "<strong>", "</strong>", "<em>", category.name, "</em>")
            flash(message, "success")
        except:
            session.rollback()
            message = "{}Whoops!{} Couldn't change name for {}{}{}.".format(
                "<strong>", "</strong>", "<em>", category.name, "</em>")
            flash(message, "danger")
        return redirect(url_for("category", id=category.id,
                                products=products, categories=categories))

    return render_template("category.html", brands=brands, category=category,
                           categories=categories)


@app.route("/category/add", methods=["GET", "POST"])
def category_add():
    brands = session.query(Brand).order_by(Brand.name.asc()).all()
    categories = session.query(Category).order_by(Category.name.asc()).all()

    if request.method == "POST":
        category = Category(name=request.form["category-name"].strip())
        session.add(category)

        try:
            session.commit()
            message = "{}More!{} Added {}{}{} to your Categories.".format(
                "<strong>", "</strong>", "<em>", category.name, "</em>")
            flash(message, "success")
        except:
            session.rollback()
            message = "{}Oh no!{} Problem adding {}{}{} to Categories.".format(
                "<strong>", "</strong>", "<em>", category.name, "</em>")
            flash(message, "danger")

        return redirect(url_for("products"))

    return render_template("category_add.html", brands=brands, categories=categories)
