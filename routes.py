from app import app
from db import db
import visits
from sqlalchemy.sql import text
from flask import redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def index():
    visits.add_visit()
    counter = visits.get_counter()
    return render_template("index.html", counter=counter)


@app.route("/login", methods=["POST"])
def login():

    notification = ""
    username = request.form["username"]
    password = request.form["password"]

    if len(username) > 20 or len(password) > 20:
        return redirect("/")
    if len(username) == 0 or len(password) == 0:
        return redirect("/")

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
            notification = "Väärä salasana."
            return render_template("/index.html", notification=notification)
        
    else:
        notification = "Käyttäjänimeä ei löytynyt."
        return render_template("/index.html", notification=notification)


@app.route("/register", methods=["GET", "POST"])
def register():
    notification = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = text("SELECT id, password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()

        if user:
            notification = "Käyttäjänimi ei valittavissa, valitse toinen."
            return render_template("/register.html", notification=notification)

        else:
            hash_value = generate_password_hash(password)
            sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()

            notification = "Käyttäjä rekisteröity, voit nyt kirjautua sisään."
            return render_template("index.html", notification=notification)

    return render_template("register.html")


@app.route("/logout")
def logout():
    if session:
        del session["username"]
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_term = request.form.get("search_term")
        if len(search_term) > 20:
            return redirect("/")
        if len(search_term) == 0:
            return redirect("/")
        
        sql = text("SELECT id, name, price, category FROM items WHERE name ILIKE :search_term")
        result = db.session.execute(sql, {"search_term": "%" + search_term + "%"})
        items_list = result.fetchall()

        return render_template("search.html", items=items_list)

    return redirect("/")


@app.route("/catalog", methods=["GET", "POST"])
def catalog():
    sort_type = request.args.get("sort_type")

    if sort_type == "name_asc":
        sql = text("""SELECT id, name, price, category, 
                   grade FROM items ORDER BY name ASC""")

    elif sort_type == "name_desc":
        sql = text("""SELECT id, name, price, category, 
                   grade FROM items ORDER BY name DESC""")

    elif sort_type == "price_asc":
        sql = text("""SELECT id, name, price, category, 
                   grade FROM items ORDER BY price ASC""")

    elif sort_type == "price_desc":
        sql = text("""SELECT id, name, price, category, 
                   grade FROM items ORDER BY price DESC""")

    elif sort_type == "most_sold":
        sql = text("""SELECT id, name, price, category, 
                   grade FROM items ORDER BY sold DESC""")

    elif sort_type == "grade":
        sql = text("""SELECT id, name, price, category, 
                   grade FROM items ORDER BY grade DESC""")

    else:
        sql = text("SELECT id, name, price, category, grade FROM items")

    result = db.session.execute(sql)
    items_list = result.fetchall()

    return render_template("catalog.html", items=items_list)


@app.route("/item/<int:item_id>")
def item_page(item_id):
    user_id = session.get("user_id")
    user_can_review = False

    sql_item = text("SELECT * FROM items WHERE id = :item_id")
    item = db.session.execute(sql_item, {"item_id": item_id}).fetchone()

    sql_grade = text("SELECT ROUND(AVG(grade),1) FROM reviews WHERE item_id = :item_id")
    avg_grade = db.session.execute(sql_grade, {"item_id": item_id}).scalar()
    if avg_grade == None:
        avg_grade = "-"

    sql_grades = text("SELECT COUNT(grade) FROM reviews WHERE item_id = :item_id")
    grades = db.session.execute(sql_grades, {"item_id": item_id}).scalar()

    sql_reviews = text("""SELECT users.username, reviews.item_id, reviews.content, reviews.grade 
    FROM reviews JOIN users ON users.id = reviews.user_id WHERE reviews.item_id = :item_id""")
    reviews = db.session.execute(sql_reviews, {"item_id": item_id}).fetchall()

    if user_id:

        sql_user = text("SELECT user_id FROM bought WHERE user_id = :user_id AND item_id = :item_id")
        is_bought = db.session.execute(sql_user, {"user_id": user_id, "item_id": item_id})

        if is_bought.fetchone():
            user_can_review = True

    return render_template("item_page.html", item=item, reviews=reviews, user_can_review=user_can_review, avg_grade=avg_grade, grades=grades)


@app.route("/cart")
def cart():
    notification = ""
    user_id = session.get("user_id")
    if user_id:
        sql_cart = text("""SELECT items.id, items.name, items.price 
        FROM cart JOIN items ON cart.item_id = items.id WHERE cart.user_id = :user_id""")
        cart_items = db.session.execute(sql_cart, {"user_id": user_id}).fetchall()

        return render_template("cart.html", cart_items=cart_items)
    
    notification = "Kirjaudu sisään nähdäksesi ostoskorin."
    return render_template("index.html", notification=notification)


@app.route("/update_cart", methods=["POST"])
def update_cart():
    option = request.form.get("option")
    item_id = request.form.get("item_id")
    user_id = session.get("user_id")

    if option == "add":
        sql_item = text("INSERT INTO cart (item_id, user_id) VALUES (:item_id, :user_id)")
        db.session.execute(sql_item, {"item_id": item_id, "user_id": user_id})
        db.session.commit()

    elif option == "remove":
        sql_item = text("DELETE FROM cart WHERE item_id = :item_id AND user_id = :user_id")
        db.session.execute(sql_item, {"item_id": item_id, "user_id": user_id})
        db.session.commit()

    return redirect(url_for("item_page", item_id=item_id))


@app.route("/purchase_items", methods=["POST"])
def purchase():
    notification = ""
    user_id = session.get("user_id")
    sql_cart = text("SELECT user_id, item_id FROM cart WHERE user_id = :user_id")
    cart_items = db.session.execute(sql_cart, {"user_id": user_id}).fetchall()

    if len(cart_items) == 0:
        notification = "Ostoskori tyhjä, ostosta ei voi suorittaa."
        return render_template("cart.html", notification=notification)

    for item in cart_items:
        sql_item = text("""INSERT INTO bought (user_id, item_id, time) 
                        VALUES (:user_id, :item_id, current_date)""")
        db.session.execute(sql_item, {"item_id": item.item_id, "user_id": user_id})

        sql_item_sold = text("""UPDATE items SET sold = sold+1 WHERE id = :item_id""")
        db.session.execute(sql_item_sold, {"item_id": item.item_id})

        db.session.commit()

    sql_cart = text("DELETE FROM cart WHERE user_id = :user_id")
    db.session.execute(sql_cart, {"user_id": user_id})
    db.session.commit()

    return render_template("purchase_made.html")


@app.route("/post_review", methods=["POST"])
def user_review():
    user_id = session.get("user_id")
    item_id = request.form.get("item_id")
    content = request.form.get("content")
    grade = request.form.get("grade")

    sql_review = text("""INSERT INTO reviews (user_id, item_id, content, grade) 
                      VALUES (:user_id, :item_id, :content, :grade)""")
    db.session.execute(sql_review, {"user_id": user_id, "item_id": item_id, "content": content, "grade": grade})
    db.session.commit()

    return redirect(url_for("item_page", item_id=item_id))


@app.route("/usersettings")
def usersettings():

    notification = ""
    is_admin = False
    user_id = session.get("user_id")
    admin_check = text("SELECT admin FROM users WHERE id = :user_id")
    admin_user = db.session.execute(admin_check, {"user_id": user_id}).scalar()

    if admin_user == True:
        is_admin = True

    if user_id:

        return render_template("usersettings.html", is_admin=is_admin)
    
    notification = "Kirjaudu sisään nähdäksesi käyttäjäasetukset."
    return render_template("index.html", notification=notification)


@app.route("/user_reviews")
def user_reviews():

    notification = ""
    user_id = session.get("user_id")
    if user_id:
        sql = text("""SELECT reviews.*, items.name AS item_name
                    FROM reviews JOIN items ON reviews.item_id = items.id 
                   WHERE reviews.user_id = :user_id""")
        user_reviews = db.session.execute(sql, {"user_id": user_id}).fetchall()

        return render_template("user_reviews.html", user_reviews=user_reviews)
    
    notification = "Kirjaudu sisään nähdäksesi käyttäjäasetukset."
    return render_template("index.html", notification=notification)


@app.route("/user_purchases")
def user_purchases():

    notification = ""
    user_id = session.get("user_id")
    if user_id:
        sql = text("""SELECT items.*, bought.time AS purchase_time
                    FROM items JOIN bought ON items.id = bought.item_id
                    WHERE bought.user_id = :user_id""")
        user_purchases = db.session.execute(sql, {"user_id": user_id}).fetchall()
        
        return render_template("user_purchases.html", user_purchases=user_purchases)
    
    notification = "Kirjaudu sisään nähdäksesi käyttäjäasetukset."
    return render_template("index.html", notification=notification)


@app.route("/all_purchases")
def all_purchases():

    is_admin = False
    user_id = session.get("user_id")
    admin_check = text("SELECT admin FROM users WHERE id = :user_id")
    admin_user = db.session.execute(admin_check, {"user_id": user_id}).scalar()

    if admin_user == True:
        is_admin = True
        sql = text("""SELECT items.*, bought.time AS purchase_time
                    FROM items JOIN bought ON items.id = bought.item_id""")
        all_purchases = db.session.execute(sql).fetchall()
        
        return render_template("all_purchases.html", all_purchases=all_purchases, is_admin=is_admin)
    
    notification = "Kirjaudu sisään nähdäksesi käyttäjäasetukset."
    return render_template("index.html", notification=notification)


@app.route("/item_tools", methods=["GET", "POST"])
def item_tools():
    notification = ""
    is_admin = False
    user_id = session.get("user_id")
    admin_check = text("SELECT admin FROM users WHERE id = :user_id")
    admin_user = db.session.execute(admin_check, {"user_id": user_id}).scalar()

    if admin_user == False:
        return render_template("usersettings.html", is_admin=is_admin)
    
    is_admin = True

    if request.method == "POST":
        item_name = request.form.get("name")
        item_price = request.form.get("price")
        item_category = request.form.get("category")

        sql_item = text("""INSERT INTO items 
        (name, price, category, time, sold, grade) 
        VALUES (:item_name, :item_price, :item_category, current_date, 0, 0)""")
        db.session.execute(sql_item, {"item_name": item_name, "item_price": item_price, "item_category": item_category})
        db.session.commit()

        notification = "Uusi tuote lisätty valikoimaan."

    sql = text("SELECT id, name, price FROM items")

    result = db.session.execute(sql)
    items_list = result.fetchall()

    return render_template("item_tools.html", notification=notification, is_admin=is_admin, items=items_list)


