import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "app.config.DevelopmentConfig")
app.config.from_object(config_path)

db = SQLAlchemy(app)
db.create_all()

from . import views
from . import filters
from . import api
from . import forms
from . import login
