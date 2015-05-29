from datetime import datetime

from flask import render_template, request, redirect, url_for, flash

from cakes import app
from cakes.database import session
from cakes.models import Brand, Category, SubCategory, Item, Notes


@app.route("/")
def home():
    return "Hello Cakes"
