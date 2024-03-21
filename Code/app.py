import database as db
import plots as plt
import jinja2
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'ojolisa112233'

db.initialize()


@app.route("/")
def home():
    username = session.get("username", "User")
    conn = sqlite3.connect("grocery.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM category")
    categories = cur.fetchall()
    products = dict()
    for category in categories:
        cur.execute("SELECT * FROM product WHERE Categoryid=?", (category[0],))
        category_products = cur.fetchall()
        products[category] = category_products
    cur.close()
    conn.close()
    return render_template("home.html", name=username, categories=categories, products=products)


@app.route("/Inventory")
def Inventory():
    username = session.get("admin", "Admin")
    return render_template("inventory.html")


@app.route("/add/<int:i>")
def addtocart(i):
    conn = sqlite3.connect("grocery.db")
    cur = conn.cursor()
    username = session.get("username", "User")
    cur.execute("SELECT Cart FROM user WHERE Username=?", (username,))
    try:
        Cart = cur.fetchone()[0]
    except:
        return render_template("userlogin.html", error="Login to add to cart.")
    Cart += ' '+str(i)+' '
    cur.execute("UPDATE user SET Cart=? WHERE Username=?", (Cart, username))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/remove/<int:i>")
def removecart(i):
    conn = sqlite3.connect("grocery.db")
    cur = conn.cursor()
    username = session.get("username", "User")
    cur.execute("SELECT Cart FROM user WHERE Username=?", (username,))
    Cart = cur.fetchone()[0]
    Cart = Cart.split()
    new = []
    for j in Cart:
        if int(j) != i:
            new.append(j)
    newcart = ''
    for j in new:
        newcart += ' '+j+' '
    cur.execute("UPDATE user SET Cart=? WHERE Username=?", (newcart, username))
    conn.commit()
    conn.close()
    return redirect("/cart")


@app.route("/cart")
def cart():
    conn = sqlite3.connect("grocery.db")
    cur = conn.cursor()
    username = session.get("username", "User")
    cur.execute("SELECT Cart FROM user WHERE Username=?", (username,))
    try:
        prod = cur.fetchone()[0]
    except:
        return render_template("userlogin.html", error="Login to view cart.")
    prod = prod.split()
    cart = []
    for i in prod:
        cur.execute("SELECT * FROM product WHERE id=?", (int(i),))
        cart.append(cur.fetchone())
    conn.close()
    total_amount = 0
    for i in cart:
        total_amount += i[5]
    return render_template("cart.html", cart=cart, total_amount=total_amount)


@app.route("/thanks")
def thanks():
    username = session.get("username", "User")
    conn = sqlite3.connect("grocery.db")
    cur = conn.cursor()
    cur.execute("SELECT Cart FROM user WHERE username=?", (username,))
    cart = cur.fetchone()[0]
    cart = cart.split()
    for i in cart:
        cur.execute(
            "UPDATE product SET quantity=quantity-1 WHERE id=?", (int(i),))
        conn.commit()
    cur.execute("UPDATE user SET Cart='' WHERE username=?", (username,))
    conn.commit()
    conn.close()
    return render_template("thanks.html", username=username)


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        name = request.form.get("product_name")
        man = request.form.get("manufacture_date")
        exp = request.form.get("expiry_date")
        category = request.form.get("category")
        rate = request.form.get("rate")
        query = "SELECT * FROM product JOIN category ON product.categoryid=category.id WHERE "
        L = []
        if name:
            query += "product.Name=?"
            L.append(name)
            if man or exp or category or rate:
                query += " AND "
        if man:
            query += "product.ManufactureDate=?"
            L.append(man)
            if exp or category or rate:
                query += " AND "
        if exp:
            query += "product.ExpiryDate=?"
            L.append(exp)
            if category or rate:
                query += " AND "
        if category:
            query += "category.Name=?"
            L.append(category)
            if rate:
                query += " AND "
        if rate:
            query += "product.rate=?"
            L.append(rate)
        conn = sqlite3.connect("grocery.db")
        cur = conn.cursor()
        cur.execute(query, tuple(L))
        products = cur.fetchall()
        conn.close()
        return render_template("search.html", products=products)
    return render_template("search.html")


@app.route("/userregister", methods=['GET', 'POST'])
def userregister():
    if request.method == "POST":
        userid = request.form.get("userid")
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("grocery.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE Username = ?", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            error_message = "Username already exists. Please choose a different username."
            return render_template("userregister.html", error=error_message)

        cur.execute("INSERT INTO user(id, Username, Password) VALUES (?, ?, ?)",
                    (userid, username, password))
        conn.commit()
        conn.close()

        return redirect(url_for("userlogin"))
    return render_template("userregister.html")


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("grocery.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM user WHERE Username = ? AND Password = ?", (username, password))
        user = cur.fetchone()

        if user:
            session['username'] = username
            return redirect(url_for("home"))
        else:
            error_message = "Invalid username or password"
            return render_template("userlogin.html", error=error_message)

    return render_template("userlogin.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    session['redirect'] = request.referrer
    return redirect(session.get('redirect') or url_for('home'))


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("grocery.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE Username = ? AND Password = ?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['admin'] = username
            return redirect(url_for("manage_inventory"))
        else:
            error_message = "Invalid username or password"
            return render_template("adminlogin.html", error=error_message)

    return render_template("adminlogin.html")


@app.route("/inventory")
def manage_inventory():
    conn = sqlite3.connect("grocery.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    cur.execute("SELECT * FROM category")
    category = cur.fetchall()
    conn.close()
    return render_template("inventory.html", products=products, category=category)


@app.route("/delete_category/<int:i>", methods=['POST', 'GET'])
def deletecat(i):
    if request.method == 'POST':
        conn = sqlite3.connect("grocery.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM category WHERE id=?", (i,))
        conn.commit()
        conn.close()
        return redirect("/inventory")


@app.route("/delete_product/<int:i>", methods=['GET', 'POST'])
def deleteprod(i):
    if request.method == 'POST':
        conn = sqlite3.connect("grocery.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM product WHERE id=?", (i,))
        conn.commit()
        conn.close()
        return redirect("/inventory")


@app.route("/add_category", methods=['POST', 'GET'])
def add_category():
    if request.method == "POST":
        id = request.form.get("category_id")
        name = request.form.get("category_name")
        image = request.form.get("category_image")
        conn = sqlite3.connect("grocery.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO category(id,Name,image) VALUES (?,?,?)", (id, name, image))
        conn.commit()
        conn.close()
        return redirect("/inventory")
    return render_template("add_category.html")


@app.route("/editcat", methods=['POST', 'GET'])
def editcat():
    if request.method == "POST":
        id = request.form.get("category_id")
        name = request.form.get("category_name")
        image = request.form.get("category_image")
        conn = sqlite3.connect("grocery.db")
        cur = conn.cursor()
        if name:
            cur.execute("UPDATE category SET Name=? WHERE id=?", (name, id))
        if image:
            cur.execute("UPDATE category SET image=? WHERE id=?", (image, id))
        conn.commit()
        conn.close()
        return redirect("/inventory")
    return render_template("editcat.html")


@app.route("/add_product", methods=['POST', 'GET'])
def add_product():
    if request.method == "POST":
        id = request.form.get("product_id")
        name = request.form.get("product_name")
        man = request.form.get("manufacture_date")
        exp = request.form.get("expiry_date")
        catid = request.form.get("category_id")
        rate = request.form.get("rate")
        unit = request.form.get("unit")
        image = request.form.get("product_image")
        quantity = request.form.get("quantity")
        conn = sqlite3.connect("grocery.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO product(id,Name,ManufactureDate,ExpiryDate,Categoryid,rate,image,quantity,unit) VALUES (?,?,?,?,?,?,?,?,?)",
                    (id, name, man, exp, catid, rate, image, quantity, unit))
        conn.commit()
        conn.close()
        return redirect("/inventory")
    return render_template("add_product.html")


@app.route("/editprod", methods=['POST', 'GET'])
def editprod():
    if request.method == "POST":
        id = request.form.get("product_id")
        name = request.form.get("product_name")
        man = request.form.get("manufacture_date")
        exp = request.form.get("expiry_date")
        catid = request.form.get("category_id")
        rate = request.form.get("rate")
        image = request.form.get("product_image")
        quantity = request.form.get("quantity")
        conn = sqlite3.connect("grocery.db")
        cur = conn.cursor()
        if name:
            cur.execute("UPDATE product SET Name=? WHERE id=?", (name, id))
        if man:
            cur.execute(
                "UPDATE product SET ManufactureDate=? WHERE id=?", (man, id))
        if exp:
            cur.execute(
                "UPDATE product SET ExpiryDate=? WHERE id=?", (exp, id))
        if catid:
            cur.execute(
                "UPDATE product SET Categoryid=? WHERE id=?", (catid, id))
        if rate:
            cur.execute("UPDATE product SET rate=? WHERE id=?", (rate, id))
        if image:
            cur.execute("UPDATE product SET image=? WHERE id=?", (image, id))
        if quantity:
            cur.execute("UPDATE product SET quantity=? WHERE id=?",
                        (quantity, id))
        conn.commit()
        conn.close()
        return redirect("/inventory")
    return render_template("editprod.html")


@app.route("/stats")
def stats():
    img1 = plt.plot1()

    return render_template("stats.html", img1=img1)


if __name__ == '__main__':
    app.run()
