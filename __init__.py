from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import auth, product, order
    app.register_blueprint(auth.bp)
    app.register_blueprint(product.bp)
    app.register_blueprint(order.bp)

    return app
