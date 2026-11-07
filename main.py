from flask import Flask, render_template, request, redirect, url_for, session, flash

from core.config import SECRET_KEY, ACCOUNT_TYPES
from core.database import init_db
from core import validators, users, products, orders

app = Flask(__name__)
app.secret_key = SECRET_KEY

init_db()


def is_logged_in(role):
    return session.get("user") is not None and session.get("role") == role


def get_form(*names):
    form = {}
    for name in names:
        form[name] = request.form.get(name, "").strip()
    return form


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = get_form("utype", "userid", "password")
        # passwords are not stripped
        form["password"] = request.form.get("password", "")

        ok, message = users.login_user(form["userid"], form["password"], form["utype"])
        if ok:
            session["user"] = form["userid"]
            session["role"] = form["utype"]
            return redirect(url_for("home"))

        flash(message, "error")
        return render_template("login.html", types=ACCOUNT_TYPES, form=form)

    return render_template("login.html", types=ACCOUNT_TYPES, form={})


@app.route("/register/customer", methods=["GET", "POST"])
def register_customer():
    if request.method == "POST":
        form = get_form("fname", "lname", "email", "phno", "address", "uid")
        pass1 = request.form.get("pass1", "")
        pass2 = request.form.get("pass2", "")

        error = validators.check_not_empty(form)
        if not error:
            error = validators.check_email(form["email"])
        if not error:
            error = validators.check_phone(form["phno"])
        if not error:
            error = validators.check_passwords(pass1, pass2)

        if not error:
            ok, message = users.register_customer(
                form["uid"], pass1, form["fname"], form["lname"],
                form["email"], form["address"], form["phno"],
            )
            if ok:
                flash(message, "success")
                return redirect(url_for("login"))
            error = message

        flash(error, "error")
        return render_template("register_customer.html", form=form)

    return render_template("register_customer.html", form={})


@app.route("/register/seller", methods=["GET", "POST"])
def register_seller():
    if request.method == "POST":
        form = get_form("name", "phno", "address", "uid")
        pass1 = request.form.get("pass1", "")
        pass2 = request.form.get("pass2", "")

        error = validators.check_not_empty(form)
        if not error:
            error = validators.check_phone(form["phno"])
        if not error:
            error = validators.check_passwords(pass1, pass2)

        if not error:
            ok, message = users.register_seller(
                form["uid"], pass1, form["name"], form["address"], form["phno"],
            )
            if ok:
                flash(message, "success")
                return redirect(url_for("login"))
            error = message

        flash(error, "error")
        return render_template("register_seller.html", form=form)

    return render_template("register_seller.html", form={})


@app.route("/home")
def home():
    if session.get("user") is None:
        return redirect(url_for("login"))

    profile = users.get_profile(session["user"], session["role"])
    if profile is None:
        session.clear()
        return redirect(url_for("login"))

    return render_template("home.html", profile=profile)


@app.route("/buy")
def buy():
    if not is_logged_in("customer"):
        return redirect(url_for("login"))

    return render_template("buy.html", items=products.get_all_products())


@app.route("/order", methods=["POST"])
def order():
    if not is_logged_in("customer"):
        return redirect(url_for("login"))

    pid = request.form.get("pid", "").strip()
    quantity_text = request.form.get("orderquantity", "").strip()

    error = validators.check_quantity(quantity_text)
    if error:
        flash(error, "error")
        return redirect(url_for("buy"))

    ok, message = orders.place_order(session["user"], pid, int(quantity_text))
    if ok:
        flash(message, "success")
        return redirect(url_for("my_orders"))

    flash(message, "error")
    return redirect(url_for("buy"))


@app.route("/orders")
def my_orders():
    if session.get("user") is None:
        return redirect(url_for("login"))

    if session["role"] == "customer":
        rows = orders.get_customer_orders(session["user"])
    else:
        rows = orders.get_seller_orders(session["user"])

    return render_template("orders.html", rows=rows)


@app.route("/seller/add", methods=["GET", "POST"])
def add_product():
    if not is_logged_in("seller"):
        return redirect(url_for("login"))

    if request.method == "POST":
        form = get_form("prname", "prid", "mfname", "mdate", "edate", "quantity", "price")

        error = validators.check_not_empty(form)
        if not error:
            error = validators.check_dates(form["mdate"], form["edate"])
        if not error:
            error = validators.check_quantity(form["quantity"])
        if not error:
            error = validators.check_price(form["price"])

        if not error:
            ok, message = products.add_product(
                session["user"], form["prid"], form["prname"], form["mfname"],
                form["mdate"], form["edate"], int(form["price"]), int(form["quantity"]),
            )
            if ok:
                flash(message, "success")
                return redirect(url_for("restock"))
            error = message

        flash(error, "error")
        return render_template("add_product.html", form=form)

    return render_template("add_product.html", form={})


@app.route("/seller/restock", methods=["GET", "POST"])
def restock():
    if not is_logged_in("seller"):
        return redirect(url_for("login"))

    if request.method == "POST":
        pid = request.form.get("pid", "").strip()
        quantity_text = request.form.get("restock", "").strip()

        error = validators.check_quantity(quantity_text)
        if error:
            flash(error, "error")
        else:
            ok, message = products.restock_product(session["user"], pid, int(quantity_text))
            flash(message, "success" if ok else "error")

        return redirect(url_for("restock"))

    return render_template("restock.html", items=products.get_seller_products(session["user"]))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
