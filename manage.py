import os

from livereload import Server
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from getpass import getpass
from werkzeug.security import generate_password_hash

from app import app, db
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
        db.session.add(brand)
        db.session.commit()
    for category_name in ['Blush', 'Bronzer', 'Concealer', 'Eyes',
                          'Highlighters', 'Lips', 'Palettes', 'Skincare']:
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()

    eyes = session.query(Category).filter_by(name="Eyes").first()
    for sub_category_name in ['Brows', 'Eye Primers', 'Eyeshadow',
                              'Eyeliner', 'Mascara']:
        sub_category = SubCategory(name=sub_category_name)
        eyes.sub_categories.append(sub_category)
        db.session.add(sub_category)
        db.session.commit()

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
    db.session.add(user)
    db.session.commit()

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
        db.session.add(user)
        db.session.commit()
    else:
        print "Could not find user {}.".format(name)
        return

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(db.metadata))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
