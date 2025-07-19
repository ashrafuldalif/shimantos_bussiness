from flask import Flask, render_template, request, redirect, url_for, session,flash
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
        product = Product.query.get((product_id))
        if product:
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({
                'id': product.product_id,
                'name': product.product_name,
                'price': product.price,
                'size': product.size,
                'color': product.color,
                'quantity':product.product_available,
                'build_cost':product.costing,
                'rate':product.rating,
                'image':product.image,
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


@app.route("/cart")
def cart():
    products = Product.query.all()
    cart = session.get('cart', {})
    cart_items = []
    total = Decimal("0.00")

    for product_id, qty in cart.items():
        product = Product.query.get((product_id))
        if product:
            subtotal = product.price * qty
            total += subtotal
            cart_items.append({
                'id': product.product_id,
                'name': product.product_name,
                'price': product.price,
                'size': product.size,
                'color': product.color,
                'quantity':product.product_available,
                'build_cost':product.costing,
                'rate':product.rating,
                'image':product.image,
                'qty': qty,
                'subtotal': subtotal
            })

    return render_template("cart.html",cart=cart_items, total=total)


@app.route("/add_to_cart_page", methods=["POST"])
def add_to_cart_page():
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity", 1))

    cart = session.get("cart", {})
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    session["cart"] = cart
    print(f"added to cart now cart item {len(cart)}")
    return redirect(url_for("cart"))


    # __tablename__ = 'product'
    # product_id = db.Column(db.Integer, primary_key=True)
    # product_name = db.Column(db.String(100), nullable=False)
    # price = db.Column(db.Numeric(10, 2), nullable=False)
    # color = db.Column(db.String(50))
    # size = db.Column(db.String(20))
    # product_available = db.Column(db.Integer)
    # costing = db.Column(db.Numeric(10, 2))
    # rating = db.Column(db.Numeric(3, 2))
    # image = db.Column(db.String(100))









@app.route("/remove_from_cart_home/<int:product_id>")
def remove_from_cart_home(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
    session['cart'] = cart
    return redirect(url_for("home"))    



@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1  # Decrement quantity by 1
        else:
            del cart[product_id_str]  # Remove item if quantity is 1

    session['cart'] = cart
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





# Admin Section
@app.route("/admin/manage-products", methods=["GET"])
def manage_products():
    products = Product.query.all()
    return render_template("admin/manageproduct.html", products=products)


@app.route("/admin/add-product", methods=["POST"])
def add_product():
    try:
        name = request.form.get("product_name")  # match your form input names
        price = Decimal(request.form.get("price"))
        color = request.form.get("color")
        size = request.form.get("size")
        quantity = int(request.form.get("product_available"))
        cost = Decimal(request.form.get("costing"))
        rating = Decimal(request.form.get("rating"))
        image = request.form.get("image")

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
            image=image
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
    except Exception as e:
        flash(f"Error adding product: {str(e)}", "error")
    return redirect(url_for("manage_products"))


@app.route("/admin/edit-product/<int:product_id>", methods=["POST"])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        product.product_name = request.form.get("product_name")
        product.price = Decimal(request.form.get("price"))
        product.color = request.form.get("color")
        product.size = request.form.get("size")
        product.product_available = int(request.form.get("product_available"))
        product.costing = Decimal(request.form.get("costing"))
        product.rating = Decimal(request.form.get("rating"))
        product.image = request.form.get("image")

        db.session.commit()
        flash("Product updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating product: {str(e)}", "error")
    return redirect(url_for("manage_products"))


@app.route("/admin/delete-product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash("Product deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting product: {str(e)}", "error")
    return redirect(url_for("manage_products"))















if __name__ == '__main__':
    app.run(debug=True)
