from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/createuser", methods=["POST"])
def createuser():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = text(
        "INSERT INTO users"
        "(username, password) VALUES (:username, :password)"
    )
    db.session.execute(sql, {"username": username, "password": hash_value})
    db.session.commit()

    fname = request.form["fname"]
    lname = request.form["lname"]
    sql = text("INSERT INTO members (fname, lname) VALUES (:fname, :lname)")
    db.session.execute(sql, {"fname": fname, "lname": lname})
    db.session.commit()

    session["username"] = username

    return redirect("/")


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
