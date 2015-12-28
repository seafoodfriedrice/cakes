import os

from livereload import Server
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from getpass import getpass
from werkzeug.security import generate_password_hash

from app import app
from app.database import Base, session
from app.models import Brand, Category, SubCategory, Product
from app.models import User


manager = Manager(app)

@manager.command
def run():
    server = Server(app.wsgi_app)
    server.watch('app/*.py')
    server.watch('app/templates/*.html')
    server.watch('app/static/css/*.css')
    server.watch('app/static/js/*.js')
    server.serve(host='0.0.0.0')

@manager.command
def seed():
    for brand_name in ['Dior', 'BY TERRY', 'Too Faced', 'Charlotte Tillbury']:
        brand = Brand(name=brand_name)
        session.add(brand)
        session.commit()

    for category_name in ['Blush', 'Bronzer', 'Concealer', 'Eyes',
                          'Highlighters', 'Lips', 'Palettes', 'Skincare']:
        category = Category(name=category_name)
        session.add(category)
        session.commit()

    eyes = session.query(Category).filter_by(name="Eyes").first()
    for sub_category_name in ['Brows', 'Eye Primers', 'Eyeshadow',
                              'Eyeliner', 'Mascara']:
        sub_category = SubCategory(name=sub_category_name)
        eyes.sub_categories.append(sub_category)
        session.add(sub_category)
        session.commit()

    byterry = session.query(Brand).filter_by(name="BY TERRY").first()
    eyeshadow = session.query(SubCategory).filter_by(name="Eyeshadow").first()
    product = Product(name='Ombre Blackstar "Color-Fix" Cream Eyeshadow',
                      price=43.50, color='Black Pearl', quantity=1,
                      notes="Cakes needs some product notes!", favorite=True)
    eyes.products.append(product)
    eyeshadow.products.append(product)
    byterry.products.append(product)
    session.add(product)
    session.commit()

@manager.command
def add_user():
    name = raw_input("Name: ")
    if session.query(User).filter_by(username=name).first():
        print "User already exists."
        return

    password = ""
    password_2 = ""
    while not (password and password_2) or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(username=name, password=generate_password_hash(password))
    session.add(user)
    session.commit()

@manager.command
def reset_pw():
    name = raw_input("Name: ")
    user = session.query(User).filter_by(username=name).first()
    if user:
        password = ""
        password_2 = ""
        while not (password and password_2) or password != password_2:
            password = getpass("Password: ")
            password_2 = getpass("Re-enter password: ")
        user.password =  password=generate_password_hash(password)
        session.add(user)
        session.commit()
    else:
        print "Could not find user {}.".format(name)
        return

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
