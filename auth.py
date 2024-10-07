from db import db
from app import app
from flask import render_template, request, redirect, session, url_for, flash
from sqlalchemy.sql import text
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash
import secrets


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
    print("user", user)
    if not user:
        flash("Invalid user")
        return redirect(url_for("index"))
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            # Token that will be checked when forms are submitted
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(url_for("index"))
        else:
            print("invalid pswd")
            flash('Invalid credentials')
            return redirect(url_for("index"))


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
