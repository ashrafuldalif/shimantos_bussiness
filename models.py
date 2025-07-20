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
    image = db.Column(db.String(100))  # Optional

    orders = db.relationship('Orders', backref='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.name}>"

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
    image = db.Column(db.String(100))

    orders = db.relationship('Orders', backref='product', lazy=True)
    history_items = db.relationship('History', backref='product', lazy=True)

    def __repr__(self):
        return f"<Product {self.product_name}>"

class History(db.Model):
    __tablename__ = 'history'

    history_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    time_order = db.Column(db.DateTime, default=datetime.utcnow)
    time_delivery = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<History {self.history_id} Product {self.product_id}>"

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # matches DB primary key
    order_id = db.Column(db.Integer)  # optional additional order number
    c_id = db.Column(db.Integer, db.ForeignKey('customer.c_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    product_quantity = db.Column(db.Integer),
    price = db.Column(db.Numeric(10, 2), nullable=False)
    order_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Order {self.id} Customer {self.c_id} Product {self.product_id}>"
