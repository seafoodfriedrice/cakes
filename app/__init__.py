import os

from flask import Flask

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "cakes.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import views
from . import filters
from . import api
from . import forms
from . import login
