from db import db
from app import app
from flask import render_template, request, redirect
from sqlalchemy.sql import text
import urllib.parse


@app.route("/")
def index():
    sql = text("SELECT name FROM classes")
    result = db.session.execute(sql)
    classes = result.fetchall()
    return render_template("index.html", classes=classes)


@app.route("/send", methods=["POST"])
def send():
    fname = request.form["fname"]
    lname = request.form["lname"]
    sql = text("INSERT INTO members (fname, lname) VALUES (:fname, :lname)")
    db.session.execute(sql, {"fname": fname, "lname": lname})
    # commit() required to persist the changes
    db.session.commit()
    return redirect("/")


# You can put variable names in your view functions
@app.route("/class/<name>")
def classes(name):
    name = urllib.parse.unquote_plus(name)
    sql = text("SELECT description from classes WHERE name=:name")
    result = db.session.execute(sql, {"name": name})
    single_row = result.fetchone()
    description = single_row.description
    return render_template("class.html", name=name, description=description)


@app.context_processor
def utility_processor():
    def encode_url(string):
        safe_string = urllib.parse.quote_plus(string)
        return safe_string
    return dict(encode_url=encode_url)
