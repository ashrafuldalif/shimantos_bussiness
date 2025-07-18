from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Product
from decimal import Decimal

app = Flask(__name__)
app.secret_key = "whatsupnigga"  # Change this to a secure random key in production!

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/void'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def home():
    products = Product.query.all()
    cart = session.get('cart', {})
    cart_items = []
    total = Decimal("0.00")

    for product_id, qty in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({
                'id': product.product_id,
                'name': product.product_name,
                'price': product.price,
                'qty': qty,
                'subtotal': subtotal
            })

    return render_template("index.html", products=products, lenn=len(products), cart=cart_items, total=total)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 1))

    cart = session.get("cart", {})
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    session["cart"] = cart
    print(f"added to cart now cart item {len(cart)}")
    return redirect(url_for("home"))

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
    session['cart'] = cart
    return redirect(url_for("home"))

    

@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/shop")
def shop():
    return render_template("shop.html")


if __name__ == '__main__':
    app.run(debug=True)
