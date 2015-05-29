from datetime import datetime

from flask import render_template, request, redirect, url_for, flash

from cakes import app
from cakes.database import session
from cakes.models import Brand, Category, SubCategory, Product, Notes


brands = session.query(Brand).order_by(Brand.name.asc()).all()
categories = session.query(Category).order_by(Category.name.asc()).all()

@app.route("/")
def home():
    products = session.query(Product).all()
    return render_template("home.html", brands=brands, products=products,
                                        categories=categories)
