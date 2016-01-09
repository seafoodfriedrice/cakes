class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://p:p@localhost:5433/cakes"
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = "848e462678fe13b9c3ae5c15d902ad15"
