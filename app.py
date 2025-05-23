from flask import Flask, render_template ,request # type: ignore

app = Flask(__name__)
products=[
    {"name":"Monkey  D Luffy", "price":5000,   "pic":"../static/iamges/Cluffy.jpg","id":1},
    {"name":"Roronoa Zoro",  "price":1500,  "pic":"../static/iamges/Czoro.jpg","id":2 },
    {"name":"sanji", "price":5000,   "pic":"../static/iamges/sanji.jpg","id":3},
    {"name":"nami",  "price":1500,  "pic":"../static/iamges/nami.jpg","id":4 },
    {"name":"ussop", "price":5000,   "pic":"../static/iamges/ussop.jpg","id":5},
    {"name":"Tony Tony Choper",  "price":1500,  "pic":"../static/iamges/choper.jpg","id":6 },
    {"name":"Nico RObin", "price":5000,   "pic":"../static/iamges/robin.jpg","id":7},
    {"name":"Franky",  "price":1500,  "pic":"../static/iamges/franky.jpg" ,"id":8},
    {"name":"Brook", "price":5000,   "pic":"../static/iamges/brook.jpg","id":9},
    {"name":"Jimbe",  "price":1500,  "pic":"../static/iamges/jimbe.jpg" ,"id":10}
]
@app.route("/")
def home():
    return render_template("index.html",p=products)
@app.route("/shop")
def shop():
    return render_template("shop.html",p=products)
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/profile")
def profile():
    return render_template("profile.html")
@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/reviews")
def reviews():
    return render_template("reviews.html")

app.run(host="0.0.0.0", port=5000, debug=True)
# app.run(debug=True)

