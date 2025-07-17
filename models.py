from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customer'
    c_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(15), nullable=False)
    gmail = db.Column(db.String(100), nullable=False)
    secret_key = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    color = db.Column(db.String(50))
    size = db.Column(db.String(20))
    product_available = db.Column(db.Integer)
    costing = db.Column(db.Numeric(10, 2))
    rating = db.Column(db.Numeric(3, 2))

class History(db.Model):
    __tablename__ = 'history'
    history_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    time_order = db.Column(db.DateTime, default=datetime.utcnow)
    time_delivery = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_id = db.Column(db.Integer, db.ForeignKey('customer.c_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    order_time = db.Column(db.DateTime, default=datetime.utcnow)
    