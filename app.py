from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from db import init_db, mysql

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "inventory_secret"

init_db(app)

# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users(username,password) VALUES(%s,%s)",
            (username, password),
        )
        mysql.connection.commit()

        flash("Registration successful. Login now.")
        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user[2], password):
            session["user"] = user[1]
            return redirect(url_for("dashboard"))

        flash("Invalid credentials")

    return render_template("login.html")

    if "user" not in session:
      return redirect(url_for("login"))



# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")

# ---------------- PRODUCTS ----------------

@app.route("/products")
def products():
    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()

    return render_template("products.html", products=data)


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        price = request.form["price"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO products(name,quantity,price) VALUES(%s,%s,%s)",
            (name, quantity, price),
        )
        mysql.connection.commit()

        return redirect(url_for("products"))

    return render_template("add_product.html")


@app.route("/delete_product/<int:id>")
def delete_product(id):
    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (id,))
    mysql.connection.commit()

    return redirect(url_for("products"))

# ---------------- EDIT PRODUCT ----------------

@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()

    # GET → fetch product
    if request.method == "GET":
        cur.execute("SELECT * FROM products WHERE id=%s", (id,))
        product = cur.fetchone()
        return render_template("edit_product.html", product=product)

    # POST → update product
    name = request.form["name"]
    quantity = request.form["quantity"]
    price = request.form["price"]

    cur.execute(
        "UPDATE products SET name=%s, quantity=%s, price=%s WHERE id=%s",
        (name, quantity, price, id),
    )
    mysql.connection.commit()

    return redirect(url_for("products"))

# ---------------- CATEGORIES ----------------

@app.route("/categories")
def categories():
    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM categories")
    data = cur.fetchall()

    return render_template("categories.html", categories=data)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO categories(name) VALUES(%s)", (name,))
        mysql.connection.commit()

        return redirect(url_for("categories"))

    return render_template("add_category.html")


@app.route("/delete_category/<int:id>")
def delete_category(id):
    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM categories WHERE id=%s", (id,))
    mysql.connection.commit()

    return redirect(url_for("categories"))


# ---------------- SUPPLIERS ----------------

@app.route("/suppliers")
def suppliers():
    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM suppliers")
    data = cur.fetchall()

    return render_template("suppliers.html", suppliers=data)


@app.route("/add_supplier", methods=["GET", "POST"])
def add_supplier():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO suppliers(name,phone,email) VALUES(%s,%s,%s)",
            (name, phone, email),
        )
        mysql.connection.commit()

        return redirect(url_for("suppliers"))

    return render_template("add_supplier.html")


@app.route("/delete_supplier/<int:id>")
def delete_supplier(id):
    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM suppliers WHERE id=%s", (id,))
    mysql.connection.commit()

    return redirect(url_for("suppliers"))



#------ Product rooute-------
@app.route("/add_product", methods=["GET", "POST"])
def add_product_new(): 

    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()

    # Get categories and suppliers for dropdown
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()

    cur.execute("SELECT * FROM suppliers")
    suppliers = cur.fetchall()

    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        price = request.form["price"]
        category_id = request.form["category"]
        supplier_id = request.form["supplier"]

        cur.execute("SELECT * FROM categories")
        categories = cur.fetchall()
        cur.execute("SELECT * FROM suppliers")
        suppliers = cur.fetchall()


        cur.execute(
            "INSERT INTO products(name,quantity,price,category_id,supplier_id) VALUES(%s,%s,%s,%s,%s)",
            (name, quantity, price, category_id, supplier_id)
        )
        mysql.connection.commit()

        return redirect(url_for("add_product_new"))

    return render_template("add_product.html", categories=categories, suppliers=suppliers)

@app.route("/add_product", methods=["GET", "POST"])
def add_product1():
    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()

    # Fetch categories and suppliers for dropdown
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur.execute("SELECT * FROM suppliers")
    suppliers = cur.fetchall()

    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        price = request.form["price"]
        category_id = request.form["category"]
        supplier_id = request.form["supplier"]

        cur.execute(
            "INSERT INTO products(name,quantity,price,category_id,supplier_id) VALUES(%s,%s,%s,%s,%s)",
            (name, quantity, price, category_id, supplier_id)
        )
        mysql.connection.commit()
        return redirect(url_for("products"))

    return render_template("add_product.html", categories=categories, suppliers=suppliers)

@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
def edit_product1(id):
    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id=%s", (id,))
    product = cur.fetchone()

    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur.execute("SELECT * FROM suppliers")
    suppliers = cur.fetchall()

    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        price = request.form["price"]
        category_id = request.form["category"]
        supplier_id = request.form["supplier"]

        cur.execute(
            "UPDATE products SET name=%s, quantity=%s, price=%s, category_id=%s, supplier_id=%s WHERE id=%s",
            (name, quantity, price, category_id, supplier_id, id)
        )
        mysql.connection.commit()
        return redirect(url_for("products"))

    return render_template("edit_product.html", product=product, categories=categories, suppliers=suppliers)

@app.route("/products1")

def products1():
    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()

    search = request.args.get("search", "")
    category = request.args.get("category", "")
    supplier = request.args.get("supplier", "")

    query = """
        SELECT p.id, p.name, p.quantity, p.price,
               c.name, s.name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN suppliers s ON p.supplier_id = s.id
        WHERE 1=1
    """

    params = []

    if search:
        query += " AND p.name LIKE %s"
        params.append(f"%{search}%")

    if category:
        query += " AND p.category_id = %s"
        params.append(category)

    if supplier:
        query += " AND p.supplier_id = %s"
        params.append(supplier)

    cur.execute(query, params)
    products = cur.fetchall()

    # dropdown data
    cur.execute("SELECT id, name FROM categories")
    categories = cur.fetchall()

    cur.execute("SELECT id, name FROM suppliers")
    suppliers = cur.fetchall()

    return render_template(
        "products.html",
        products=products,
        categories=categories,
        suppliers=suppliers,
    )

@app.route("/stock/<int:product_id>", methods=["GET", "POST"])
def stock(product_id):

    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()

    if request.method == "POST":
        qty = int(request.form["qty"])
        action = request.form["action"]
        note = request.form["note"]

        # current stock
        cur.execute("SELECT quantity FROM products WHERE id=%s", (product_id,))
        current = cur.fetchone()[0]

        if action == "OUT" and qty > current:
            flash("Not enough stock!")
            return redirect(request.url)

        new_qty = current + qty if action == "IN" else current - qty

        cur.execute(
            "UPDATE products SET quantity=%s WHERE id=%s",
            (new_qty, product_id),
        )

        cur.execute(
            """
            INSERT INTO stock_logs
            (product_id, change_qty, action, note)
            VALUES (%s,%s,%s,%s)
            """,
            (product_id, qty, action, note),
        )

        mysql.connection.commit()

        return redirect(url_for("products"))

    cur.execute("SELECT name, quantity FROM products WHERE id=%s", (product_id,))
    product = cur.fetchone()

    return render_template("stock.html", product=product)

@app.route("/stock_history")
def stock_history():

    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT s.id, p.name, s.change_qty,
               s.action, s.note, s.created_at
        FROM stock_logs s
        JOIN products p ON s.product_id = p.id
        ORDER BY s.created_at DESC
    """)

    logs = cur.fetchall()

    return render_template("stock_history.html", logs=logs)

@app.route("/sell/<int:product_id>", methods=["GET", "POST"])
def sell_product(product_id):

    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()

    if request.method == "POST":
        qty = int(request.form["qty"])
        customer = request.form["customer"]

        cur.execute("SELECT quantity FROM products WHERE id=%s", (product_id,))
        stock = cur.fetchone()[0]

        if qty > stock:
            flash("Not enough stock!")
            return redirect(request.url)

        new_qty = stock - qty

        cur.execute(
            "UPDATE products SET quantity=%s WHERE id=%s",
            (new_qty, product_id),
        )

        cur.execute(
            "INSERT INTO sales (product_id, quantity, customer_name) VALUES (%s,%s,%s)",
            (product_id, qty, customer),
        )

        cur.execute(
            """
            INSERT INTO stock_logs
            (product_id, change_qty, action, note)
            VALUES (%s,%s,'OUT',%s)
            """,
            (product_id, qty, f"Sold to {customer}"),
        )

        mysql.connection.commit()

        return redirect(url_for("products"))

    cur.execute("SELECT name, quantity FROM products WHERE id=%s", (product_id,))
    product = cur.fetchone()

    return render_template("sell.html", product=product)

@app.route("/sales")
def sales_history():

    if "user" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()

    search = request.args.get("search", "")

    query = """
        SELECT s.id, p.name, s.quantity,
               s.customer_name, s.created_at
        FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE 1=1
    """

    params = []

    if search:
        query += " AND p.name LIKE %s"
        params.append(f"%{search}%")

    query += " ORDER BY s.created_at DESC"

    cur.execute(query, params)

    sales = cur.fetchall()

    return render_template("sales.html", sales=sales)



# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
