import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/cakes"
    DEBUG = True
    SECRET_KEY = "848e462678fe13b9c3ae5c15d902ad15"
