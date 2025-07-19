from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import Customer, db, Product, Orders, History  # Added History import

from decimal import Decimal
from werkzeug.utils import secure_filename
import os
import secrets
import string

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Secure random key

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/void'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Image upload config
UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def to_decimal(val):
    try:
        return Decimal(val)
    except:
        return Decimal("0.00")



# -------------------------------- Routes --------------------------------

@app.route("/")
def home():
    products = Product.query.all()
    cart = session.get('cart', {})
    cart_items = []
    total = Decimal("0.00")

    for product_id_str, qty in cart.items():
        product = Product.query.get(int(product_id_str))
        if product:
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({
                'id': product.product_id,
                'name': product.product_name,
                'price': product.price,
                'size': product.size,
                'color': product.color,
                'quantity': product.product_available,
                'build_cost': product.costing,
                'rate': product.rating,
                'image': product.image,
                'qty': qty,
                'subtotal': subtotal
            })

    return render_template("index.html", products=products, lenn=len(products), cart=cart_items, total=total)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 1))
    cart = session.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    session["cart"] = cart
    flash("Product added to cart.", "success")
    return redirect(url_for("home"))

@app.route("/cart")
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = Decimal("0.00")

    for product_id_str, qty in cart.items():
        product = Product.query.get(int(product_id_str))
        if product:
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({
                'id': product.product_id,
                'name': product.product_name,
                'price': product.price,
                'size': product.size,
                'color': product.color,
                'quantity': product.product_available,
                'build_cost': product.costing,
                'rate': product.rating,
                'image': product.image,
                'qty': qty,
                'subtotal': subtotal
            })

    return render_template("cart.html", cart=cart_items, total=total)

@app.route("/add_to_cart_page", methods=["POST"])
def add_to_cart_page():
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 1))
    cart = session.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    session["cart"] = cart
    flash("Product quantity updated in cart.", "success")
    return redirect(url_for("cart"))

@app.route("/remove_from_cart_home/<int:product_id>")
def remove_from_cart_home(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    flash("Product removed from cart.", "info")
    return redirect(url_for("home"))

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            cart.pop(pid)
        session['cart'] = cart
        flash("Product quantity decreased.", "info")
    else:
        flash("Product not found in cart.", "warning")
    return redirect(url_for("cart"))

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/admin")
def admin():
    return render_template("adminpanel.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

#----------------------------------- Order Tracking -------------------------------------

@app.route('/place_order', methods=['POST'])
def place_order():
    cart = session.get('cart', {})

    if not cart:
        flash("Your cart is empty. Please add products before placing an order.", "error")
        return redirect(url_for('cart'))

    # For demo, using fixed customer_id; replace with actual login session
    customer_id = 1

    try:
        # Insert one order record per quantity unit
        for product_id_str, qty in cart.items():
            product_id = int(product_id_str)
            product = Product.query.get(product_id)
            if not product:
                continue
            for _ in range(qty):
                order = Orders(
                    c_id=customer_id,
                    product_id=product_id,
                    price=product.price
                )
                db.session.add(order)

        db.session.commit()
        session['cart'] = {}

        flash("Order placed successfully!", "success")
        return redirect(url_for('track_orders', c_id=customer_id))

    except Exception as e:
        db.session.rollback()
        flash(f"Failed to place order: {e}", "error")
        return redirect(url_for('cart'))

@app.route('/track_orders/<int:c_id>')
def track_orders(c_id):
    customer = Customer.query.get_or_404(c_id)
    orders = Orders.query.filter_by(c_id=c_id).all()

    tracking_data = []
    for order in orders:
        product = Product.query.get(order.product_id)
        history = History.query.filter_by(product_id=product.product_id).order_by(History.time_order.desc()).first()

        tracking_data.append({
            'product_name': product.product_name,
            'order_time': order.order_time,
            'status': history.status if history else 'Unknown',
            'price': order.price
        })

    return render_template('track_orders.html', customer=customer, tracking_data=tracking_data)

# -------------------------------- Customer Registration --------------------------------

@app.route("/customer/register", methods=["GET", "POST"])
def check_customer_email():
    if request.method == "POST":
        email = request.form.get("gmail")
        existing = Customer.query.filter_by(gmail=email).first()
        if existing:
            return redirect(url_for("checkout_page", customer_id=existing.c_id))
        else:
            return render_template("customer_register.html", gmail=email, show_form=True)
    return render_template("customer_register.html", show_form=False)

@app.route("/customer/register/submit", methods=["POST"])
def register_customer():
    try:
        name = request.form.get("name")
        address = request.form.get("address")
        number = request.form.get("number")
        gmail = request.form.get("gmail")
        image_file = request.files.get("image")

        # Auto-generate secret key
        secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))

        image_filename = None
        if image_file and image_file.filename and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            ext = os.path.splitext(filename)[1]
            image_filename = f"{secrets.token_hex(8)}{ext}"
            path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            image_file.save(path)

        new_customer = Customer(
            name=name,
            address=address,
            number=number,
            gmail=gmail,
            secret_key=secret_key,
            image=image_filename
        )
        db.session.add(new_customer)
        db.session.commit()

        return redirect(url_for("checkout_page", customer_id=new_customer.c_id))
    except Exception as e:
        flash(f"Registration failed: {e}", "error")
        return redirect(url_for("check_customer_email"))

@app.route("/checkout/<int:customer_id>")
def checkout_page(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    cart = session.get('cart', {})
    cart_items = []
    total = Decimal("0.00")

    for product_id_str, qty in cart.items():
        product = Product.query.get(int(product_id_str))
        if product:
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({
                'id': product.product_id,
                'name': product.product_name,
                'price': product.price,
                'size': product.size,
                'color': product.color,
                'quantity': product.product_available,
                'build_cost': product.costing,
                'rate': product.rating,
                'image': product.image,
                'qty': qty,
                'subtotal': subtotal
            })

    return render_template("checkout.html", customer=customer, cart=cart_items, total=total)

# -------------------------------- Admin: Product Management --------------------------------

@app.route("/admin/manage-products")
def manage_products():
    products = Product.query.all()
    return render_template("admin/manageproduct.html", products=products)

@app.route("/admin/add-product", methods=["POST"])
def add_product():
    try:
        name = request.form.get("product_name")
        price = to_decimal(request.form.get("price"))
        color = request.form.get("color")
        size = request.form.get("size")
        quantity = int(request.form.get("product_available"))
        cost = to_decimal(request.form.get("costing"))
        rating = to_decimal(request.form.get("rating"))
        image_file = request.files.get("image")

        if not name or price is None:
            flash("Name and price are required.", "error")
            return redirect(url_for("manage_products"))

        new_product = Product(
            product_name=name,
            price=price,
            color=color,
            size=size,
            product_available=quantity,
            costing=cost,
            rating=rating,
            image=None
        )
        db.session.add(new_product)
        db.session.commit()

        if image_file and allowed_file(image_file.filename):
            filename = f"{new_product.product_id}.png"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image_file.save(image_path)
            new_product.image = filename
            db.session.commit()

        flash("Product added successfully!", "success")

    except Exception as e:
        flash(f"Error adding product: {str(e)}", "error")

    return redirect(url_for("manage_products"))

@app.route("/admin/edit_product/<int:product_id>", methods=["POST"])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        product.product_name = request.form.get("product_name")
        product.price = to_decimal(request.form.get("price"))
        product.color = request.form.get("color")
        product.size = request.form.get("size")
        product.product_available = int(request.form.get("product_available") or 0)
        product.rating = to_decimal(request.form.get("rating"))
        db.session.commit()
        flash("Product updated successfully", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating product: {e}", "error")
    return redirect(url_for('manage_products'))

@app.route("/admin/delete-product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        if product.image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
            if os.path.exists(image_path):
                os.remove(image_path)
        db.session.delete(product)
        db.session.commit()
        flash("Product deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting product: {str(e)}", "error")
    return redirect(url_for("manage_products"))

# -------------------------------- Run the App --------------------------------

if __name__ == '__main__':
    app.run(debug=True)
