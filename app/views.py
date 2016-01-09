from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, login_required,\
                            current_user
from werkzeug.security import check_password_hash

from app import app, db
from .forms import ProductForm, CategoryForm
from .models import Brand, Category, Subcategory, Product, User
from .utils import flash_errors


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
    return render_template("login.html")

@app.route("/")
@app.route("/products", methods=["GET"])
#@login_required
def products():
    products = Product.query.order_by(Product.id.desc()).all()
    form = ProductForm()
    return render_template("products.html", products=products, form=form)

@app.route("/products/add", methods=["GET", "POST"])
#@login_required
def product_add():
    form = ProductForm()
    product = Product()
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("products_get"))
    else:
        flash_errors(form)
    return render_template("product.html", form=form)


@app.route("/products/<int:id>", methods=["GET", "POST"])
#@login_required
def product_get(id):
    product = Product.query.get(id)
    form = ProductForm(obj=product)
    return render_template("product.html", form=form)

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

    return render_template("brand_add.html", brands=brands,
                           categories=categories)



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


@app.route("/categories/add", methods=["GET", "POST"])
@login_required
def category_add():
    categories = Category.query.order_by(Category.name.asc()).all()
    form = CategoryForm()
    subcategory = Subcategory()
    category = Category()
    if form.validate_on_submit() and request.method == "POST":
        if form.subcategories.data.strip():
            category = (Category.query.filter(Category.name == form.name.data)
                        .first())
            subcategory.name = form.subcategories.data
            category.subcategories.append(subcategory)
        del form.subcategories
        form.populate_obj(category)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    else:
        flash_errors(form)
    return render_template("category_add.html", categories=categories,
                           form=form)

@app.route("/categories")
def categories():
    c = [category.name for category in Category.query.all()]
    return ', '.join(c)
