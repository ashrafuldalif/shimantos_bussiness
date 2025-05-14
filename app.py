from flask import Flask, render_template # type: ignore

app = Flask(__name__)
products=[
    {"name":"Monkey  D Luffy", "price":5000,   "pic":"../static/iamges/Cluffy.jpg"},
    {"name":"Roronoa Zoro",  "price":1500,  "pic":"../static/iamges/Czoro.jpg" },
    {"name":"sanji", "price":5000,   "pic":"../static/iamges/sanji.jpg"},
    {"name":"nami",  "price":1500,  "pic":"../static/iamges/nami.jpg" },
    {"name":"ussop", "price":5000,   "pic":"../static/iamges/ussop.jpg"},
    {"name":"Tony Tony Choper",  "price":1500,  "pic":"../static/iamges/choper.jpg" },
    {"name":"Nico RObin", "price":5000,   "pic":"../static/iamges/robin.jpg"},
    {"name":"Franky",  "price":1500,  "pic":"../static/iamges/franky.jpg" },
    {"name":"Brook", "price":5000,   "pic":"../static/iamges/brook.jpg"},
    {"name":"Jimbe",  "price":1500,  "pic":"../static/iamges/jimbe.jpg" }


]
@app.route("/")
def home():
    return render_template("index.html",p=products)


app.run(debug=True)

