from flask import Flask, render_template # type: ignore

app = Flask(__name__)
products=[
    {"name":"monkey  D Luffy", "price":5000,   "pic":"../static/iamges/Cluffy.jpg"},
    {"name":"Roronoa Zoro",  "price":1500,  "pic":"../static/iamges/Czoro.jpg" }

]
@app.route("/")
def home():
    return render_template("index.html",p=products)


app.run(debug=True ,use_reloader=True)

