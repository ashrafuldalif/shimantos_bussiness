from datetime import datetime
import random
from flask import Flask, render_template,abort, render_template_string, request, redirect, url_for, session, flash
from models import Customer, db, Product, Orders, History  # Added History import

from decimal import Decimal
from werkzeug.utils import secure_filename
import os
import secrets
import string

app = Flask(__name__)
app.secret_key = secrets.token_hex(10)  # Secure random key

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
    idtok = len(cart)
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

    return render_template("cart.html", cart=cart_items, total=total, idtok=idtok)

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

# -------------------------------- Customer Registration --------------------------------


def place_order(c_id):
    cart = session.get('cart', {})
    if not cart:
        flash("Your cart is empty.", "error")
        return

    new_order_id = random.randint(100000, 999999)  # or use your preferred order ID generation logic

    for product_id_str, qty in cart.items():
        product_id = int(product_id_str)
        product = Product.query.get(product_id)

        if product:
            order = Orders(
                order_id=new_order_id,
                c_id=c_id,
                product_id=product.product_id,
                product_quantity=qty,  # updated to store quantity directly
                price=product.price * qty  # total price for that product qty
            )
            db.session.add(order)

    db.session.commit()
    session.pop('cart', None)  # clear cart after placing order
    flash("Order placed successfully!", "success")












@app.route("/customer/register", methods=["GET", "POST"])
def check_customer_email():

    if request.method == "GET":
        cartsize = request.args.get("XYZ")
        cart = session.get('cart', {})
        if(str(len(cart))!=(cartsize)):
            return redirect(url_for('home'))

    if request.method == "POST":
        email = request.form.get("gmail")
        customer = Customer.query.filter_by(gmail=email).first()
        existing = Customer.query.filter_by(gmail=email).first()
        if existing:
            return redirect(url_for("checkout_page",  c_id=customer.c_id))

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

      
        # if image_file and image_file.filename and allowed_file(image_file.filename):
        #     filename = secure_filename(image_file.filename)
        #     ext = os.path.splitext(filename)[1]
        #     image_filename = f"{secrets.token_hex(8)}{ext}"
        #     path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        #     os.makedirs(os.path.dirname(path), exist_ok=True)
        #     image_file.save(path)


        new_customer = Customer(
            name=name,
            address=address,
            number=number,
            gmail=gmail,
            secret_key=secret_key,
            image=None
        )
        db.session.add(new_customer)
        db.session.commit()


        if image_file and allowed_file(image_file.filename):
            filename = f"{new_customer.c_id}.png"
            image_path = os.path.join(app.root_path, 'static', 'profile', filename)  # <-- just added 'profile'
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image_file.save(image_path)
            new_customer.image = filename
            db.session.commit()

        return redirect(url_for("checkout_page", c_id= new_customer.c_id))
    
    except Exception as e:
        flash(f"Registration failed: {e}", "error")
        return redirect(url_for("check_customer_email"))




@app.route("/checkout/<int:c_id>", methods=["GET", "POST"])
def checkout_page(c_id):
    customer = Customer.query.get_or_404(c_id)
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
                'qty': qty,
                'subtotal': subtotal
            })

    if request.method == "POST":
        card_number = request.form.get("card_number")
        exp_date = request.form.get("exp_date")
        cvv = request.form.get("cvv")

        if not card_number or not exp_date or not cvv:
            flash("Please fill all payment details", "error")
        else:
            flash("Payment successful (Demo)", "success")
            

            place_order(c_id)
            return redirect(url_for("track_page",c_id=c_id))

    return render_template("checkout.html", customer=customer, cart=cart_items, total=total)


@app.route("/tract_order/<int:c_id>", methods=["GET", "POST"])
def track_page(c_id):
    customer = Customer.query.get_or_404(c_id)

    # Get cart from session (if you want to show current cart summary)
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

    # Get all orders for this customer
    orders_raw = Orders.query.filter_by(c_id=c_id).all()

    orders = []
    for order in orders_raw:
        product = Product.query.get(order.product_id)

        # Fetch the latest history record for this product & order (if your history tracks per order)
        # If History links only to product, this will fetch the latest status for that product in general.
        # You might want to consider adding order_id in History for more precise tracking.
        history = History.query.filter_by(product_id=order.product_id).order_by(History.time_order.desc()).first()
        status = history.status if history else "Unknown"

        orders.append({
            'id': order.id,
            'order_id': order.order_id,
            'product_name': product.product_name if product else "Unknown",
            'image': product.image if product else None,
            'order_time': order.order_time,
            'status': status,
            'price': order.price,
            'quantity': order.product_quantity
        })

    return render_template(
        "track_orders.html",
        customer=customer,
        cart=cart_items,
        total=total,
        orders=orders
    )



@app.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    order = Orders.query.get_or_404(order_id)

    # Check if order is already delivered or cancelled
    # You may want to prevent cancelling delivered orders
    history = History.query.filter_by(product_id=order.product_id).order_by(History.time_order.desc()).first()
    if history and history.status == 'Delivered':
        flash("Delivered orders cannot be cancelled.", "warning")
        return redirect(url_for('track_page', c_id=order.c_id))

    # Update status in History or create new cancelled history entry
    if history:
        history.status = 'Cancelled'
        db.session.commit()
    else:
        # create new history record if none exist
        new_history = History(
            product_id=order.product_id,
            time_order=order.order_time,
            time_delivery=None,
            status='Cancelled',
            price=order.price
        )
        db.session.add(new_history)
        db.session.commit()

    flash("Order cancelled successfully.", "success")
    return redirect(url_for('track_page', c_id=order.c_id))
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
