import re
from datetime import datetime

from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import current_user
from sqlalchemy import exc
from sqlalchemy import func
from werkzeug.security import check_password_hash

from cakes import app
from cakes.database import session
from cakes.models import Brand, Category, SubCategory, Product
from cakes.models import User
from cakes.forms import ProductForm



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = session.query(User).filter(
            User.username == username).first()
        if not user or not check_password_hash(user.password,
                                                   password):
            flash("Incorrect username or password", "danger")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(request.args.get("next") or url_for("products"))
    else:
        return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    if current_user.is_authenticated():
        logout_user()
        return render_template("logout.html")
    else:
        return render_template("login.html")


@app.route("/")
@app.route("/products")
@login_required
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

@app.route("/product/add", methods=["GET", "POST"])
@login_required
def product_add():
    form = ProductForm()

    if form.validate_on_submit():
        product = Product()
        for field in ['category', 'brand', 'name', 'color', 'quantity',
                      'price', 'favorite', 'notes']:
            setattr(product, field, getattr(form, field).data)

        session.add(product)
        session.commit()

        product_href = url_for("product_edit", id=product.id)
        message = ("{}Mine!{} Added {} {} <a href='{}' class='alert-link'>{}"
            "</a> to your collection.").format("<strong>", "</strong>",
            form.brand.data, product.name, product_href, product.color)
        flash(message, "success")

        if request.form["submit"] == "Add":
            return redirect(url_for("products"))
        # Redirect back to product_add() when
        # Add Another button is pressed
        else:
            # Clear out the color form so we can quickly add
            # products that are similar in category and brand
            form.color.data = None
            return render_template("product.html", form=form, action="Add")
    else:
        flash_form_errors(form)

    return render_template("product.html", form=form, action="Add")


@app.route("/product/<int:id>", methods=["GET", "POST"])
@login_required
def product_edit(id):
    product = session.query(Product).get(id)
    form = ProductForm(obj=product)

    if request.method == "POST" and form.validate_on_submit():
        for field in ['category', 'brand', 'name', 'color', 'quantity',
                      'price', 'favorite', 'notes']:
            setattr(product, field, getattr(form, field).data)

        session.add(product)
        session.commit()

        message = "{}Done!{} Edited {} {} {}{}{} successfully.".format(
            "<strong>", "</strong>", form.brand.data, product.name,
            '<a href="#" class="alert-link">', product.color, "</a>")
        flash(message, "success")
        return redirect(url_for("products"))
    else:
        flash_form_errors(form)

    return render_template("product.html", form=form, action="Edit")


@app.route("/products/brands/<int:id>", methods=["GET", "POST"])
@login_required
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
@login_required
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
@login_required
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
@login_required
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
