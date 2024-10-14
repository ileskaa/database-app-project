from db import db
from app import app
from flask import render_template, request, redirect, session, url_for, flash
from sqlalchemy.sql import text
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash
import secrets


def create_session(username: str, is_admin: bool):
    session["username"] = username
    session["is_admin"] = is_admin
    # Token that will be checked when forms are submitted
    session["csrf_token"] = secrets.token_hex(16)


def render_with_error(errormsg: str):
    return render_template("signup.html", error=errormsg)


def get_next_member_id():
    sql = text("SELECT COUNT(*) FROM members")
    member_count = db.session.execute(sql).fetchone().count
    return member_count + 1


def createuser():
    # Save member data
    member_id = get_next_member_id()
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    sql = text(
        "INSERT INTO members(id, fname, lname, email) \
            VALUES (:id, :fname, :lname, :email)"
    )
    db.session.execute(sql, {
        "id": member_id, "fname": fname, "lname": lname, "email": email
    })
    # Save auth data
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = text(
        "INSERT INTO users(username, password, admin, member_id) \
            VALUES (:username, :password, FALSE, :member_id)"
    )
    try:
        db.session.execute(sql, {
            "username": username,
            "password": hash_value,
            "member_id": member_id
        })
    except exc.DataError:
        error = "The username should not exceed 35 characters"
        return render_with_error(error)
    except exc.IntegrityError:
        error = "The username " + username + " is already registered"
        return render_with_error(error)
    db.session.commit()  # Emables you to perform transactions
    create_session(username, False)
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
    sql = text("SELECT password, admin FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        # Note that flash messages make use of the session cookie
        flash("Invalid user")
        return redirect(url_for("index"))
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            is_admin = user.admin
            create_session(username, is_admin)
            return redirect(url_for("index"))
        else:
            flash('Invalid credentials')
            return redirect(url_for("index"))


@app.route("/logout")
def logout():
    # Remove both the username and the csrf_token
    session.clear()
    return redirect("/")
