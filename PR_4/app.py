from flask import Flask
from db import db
from resources.item import item_blueprint
from resources.store import store_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Инициализация базы данных

    app.register_blueprint(item_blueprint, url_prefix="/item")
    app.register_blueprint(store_blueprint, url_prefix="/store")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
