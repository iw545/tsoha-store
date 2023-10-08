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
            session["user_id"] = user.id
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
        
        sql = text("SELECT id, name, price FROM items WHERE name ILIKE :search_term")
        result = db.session.execute(sql, {"search_term": "%" + search_term + "%"})
        items_list = result.fetchall()

        return render_template("search.html", items=items_list)

    return redirect("/catalog")


@app.route("/catalog")
def catalog():
    # todo: add item sorting by price, category, reviews, date added, most sold
    sql = text("SELECT id, name, price FROM items")
    result = db.session.execute(sql)
    items_list = result.fetchall()

    return render_template("catalog.html", items=items_list)


@app.route("/item/<int:item_id>")
def item_page(item_id):
    current_user = session.get("user_id")
    user_can_review = False

    sql_item = text("SELECT * FROM items WHERE id = :item_id")
    item = db.session.execute(sql_item, {"item_id": item_id}).fetchone()

    # todo: fix, doesnt show reviews on item page
    sql_reviews = text("SELECT user_id, item_id, content, grade FROM reviews WHERE item_id = :item_id")
    reviews = db.session.execute(sql_reviews, {"item_id": item_id})
    reviews_list = reviews.fetchall()

    if current_user:
        # todo: check if user has bought item before
        # to allow them to write a review for an item

        #sql_user = text("SELECT user_id FROM bought WHERE user_id = :user_id AND item_id = :item_id")
        # is_bought = db.session.execute(sql_user, {"user_id": current_user, "item_id": item_id})

        # if is_bought.fetchone():
        user_can_review = True

    return render_template("item_page.html", item=item, reviews_list=reviews_list, user_can_review=user_can_review)


@app.route("/cart")
def cart():
    current_user = session.get("user_id")
    if current_user:
        sql_cart = text("SELECT item_id FROM cart")
        cart_items = db.session.execute(sql_cart)

        return render_template("cart.html", cart_items=cart_items)

    # not logged in as a user
    # display message to log in
    return redirect("/")


@app.route("/update_cart", methods=["POST"])
def update_cart():
    option = request.form.get("option")
    item_id = request.form.get("item_id")

    # add item to cart
    if option == "add":
        sql_item = text("INSERT INTO cart (item_id) VALUES (:item_id)")
        db.session.execute(sql_item, {"item_id": item_id})
        db.session.commit()

    # remove item from cart
    # todo: display item quantities and allow multiple of same item to be added
    elif option == "remove":
        sql_item = text("DELETE FROM cart WHERE item_id = :item_id")
        db.session.execute(sql_item, {"item_id": item_id})
        db.session.commit()
        
    return redirect("/cart")


@app.route("/purchase_items", methods=["POST"])
def purchase():

    sql_cart = text("SELECT user_id, item_id FROM cart")
    cart_items = db.session.execute(sql_cart)
    # add the cart items to bought table
    for item in cart_items:
        sql_item = text("INSERT INTO bought (user_id, item_id, time) VALUES (:user_id, :item_id, current_date)")
        db.session.execute(sql_item, {"item_id": item.item_id})
    db.session.commit()

    # after the above, remove items from cart
    sql_cart = text("DELETE FROM cart")
    db.session.execute(sql_cart)
    db.session.commit()

    return render_template("purchase_made.html")


@app.route("/post_review", methods=["POST"])
def user_review():
    content = request.form.get("content")
    grade = request.form.get("grade")

    sql_review = text("INSERT INTO reviews (content, grade) VALUES (:content, :grade)")
    db.session.execute(sql_review, {"content": content, "grade": grade})
    db.session.commit()

    return redirect("/")


@app.route("/usersettings")
def usersettings():
    # todo: add option to view previous orders made by user,
    # show item reviews written by user
    # if admin user: add functionality to add and remove
    # items from the database via admin settings section
    return render_template("usersettings.html")