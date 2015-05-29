import os
from flask.ext.script import Manager
from cakes import app
from cakes.database import Base, session
from cakes.models import Brand, Category, SubCategory, Product


manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

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
                      price=43.50, color='Black Pearl')
    eyes.products.append(product)
    eyeshadow.products.append(product)
    byterry.products.append(product)
    session.add(product)
    session.commit()

if __name__ == "__main__":
    manager.run()
