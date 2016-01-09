import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

config_path = os.environ.get("CONFIG_PATH", "app.config.DevelopmentConfig")
app.config.from_object(config_path)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)

from . import api
from . import filters
from . import forms
from . import login
from . import views
