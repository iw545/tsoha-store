from app import app
from db import db
import visits
from sqlalchemy.sql import text
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def index():
    visits.add_visit()
    counter = visits.get_counter()
    return render_template("index.html", counter=counter)

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if user:
        hash_value = user.password

        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
    
        else:
            # wrong password
            return redirect("/")
        
    else:
        # username not found
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = text("SELECT id, password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()

        if user:
            # Username unavailable, choose a different one.
            return redirect("/register")

        else:
            hash_value = generate_password_hash(password)
            sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()
            # Account registered.
            return redirect("/")

    return render_template("register.html")


@app.route("/logout")
def logout():
    if session:
        del session["username"]
    # todo: empty cart automatically if it has items
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_term = request.form.get("search_term")
        if len(search_term) == 0:
            return redirect("/catalog")
        
        sql = text("SELECT name, price FROM items WHERE name ILIKE :search_term")
        result = db.session.execute(sql, {"search_term": "%" + search_term + "%"})

        items_list = []
        for item in result.fetchall():
            items_list.append((item[0], item[1]))

        return render_template("search.html", items=items_list)

    return redirect("/catalog")

@app.route("/catalog")
def catalog():
    # todo: add item sorting by price, category, reviews, date added, most sold
    sql = text("SELECT name, price FROM items")
    result = db.session.execute(sql)

    items_list = []
    for item in result.fetchall():
        items_list.append((item[0], item[1]))

    return render_template("catalog.html", items=items_list)

@app.route("/cart")
def cart():
    # todo: add options:
    # - add / remove item to / from cart
    # - view cart contents
    # - purchase items in cart, add order to users purchase history
    return render_template("cart.html")

@app.route("/usersettings")
def usersettings():
    # todo: add option to view previous orders made by user,
    # show item reviews written by user
    return render_template("usersettings.html")