from db import db
from app import app
from flask import render_template, request, redirect, session
from sqlalchemy.sql import text
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():
    fname = request.form["fname"]
    lname = request.form["lname"]
    sql = text("INSERT INTO members (fname, lname) VALUES (:fname, :lname)")
    db.session.execute(sql, {"fname": fname, "lname": lname})
    # commit() required to persist the changes
    db.session.commit()
    return redirect("/")


def createuser():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = text(
        "INSERT INTO users"
        "(username, password) VALUES (:username, :password)"
    )
    try:
        db.session.execute(sql, {"username": username, "password": hash_value})
    except exc.DataError:
        error = "The username should not exceed 35 characters"
        return render_template("signup.html", error=error)

    fname = request.form["fname"]
    lname = request.form["lname"]
    sql = text("INSERT INTO members (fname, lname) VALUES (:fname, :lname)")
    try:
        db.session.execute(sql, {"fname": fname, "lname": lname})
    except exc.DataError:
        error = "The username should not exceed 35 characters"
        return render_template("signup.html", error=error)

    db.session.commit()

    session["username"] = username

    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        return createuser()
    else:
        return render_template("signup.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        print("invalid user")
        return render_template("index.html", error="Invalid credentials")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            print("invalid pswd")
            return render_template("index.html", error="Invalid credentials")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
