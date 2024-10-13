from db import db
from app import app
from flask import (
    render_template, request, redirect, session, abort, flash, url_for
)
from sqlalchemy.sql import text
import urllib.parse


@app.route("/")
def index():
    sql = text("SELECT name FROM classes")
    result = db.session.execute(sql)
    classes = result.fetchall()
    if session:
        username = session['username']
        sql = text("SELECT admin FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        is_admin = result.fetchone().admin
        return render_template(
            "index.html", classes=classes, is_admin=is_admin
        )
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
    if not session:
        abort(401)
    classname = urllib.parse.unquote_plus(name)
    sql = text("SELECT description from classes WHERE name=:classname")
    result = db.session.execute(sql, {"classname": classname})
    single_row = result.fetchone()
    description = single_row.description
    # Check if user is already registered to that class
    sql = text("SELECT COUNT(*) FROM enrollments \
        WHERE username=:username AND class=:classname")
    username = session["username"]
    result = db.session.execute(sql, {
        "username": username,
        "classname": classname
    })
    single_row = result.fetchone()
    is_registered = single_row.count
    return render_template(
        "class.html",
        classname=classname,
        description=description,
        is_registered=is_registered
    )


@app.route("/class/signup", methods=["POST"])
def class_signup():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    # Save registration to database
    selected_class = request.form["class"]
    username = session["username"]
    sql = text("INSERT INTO enrollments VALUES (:class, :username)")
    db.session.execute(sql, {"class": selected_class, "username": username})
    db.session.commit()
    origin = request.environ['HTTP_REFERER']
    return redirect(origin)


@app.route("/class/cancel", methods=["POST"])
def cancel_class():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    username = session["username"]
    class_to_cancel = request.form["class"]
    sql = text("DELETE FROM enrollments WHERE username=:username \
                AND class=:class_to_cancel")
    db.session.execute(sql, {
        "username": username, "class_to_cancel": class_to_cancel
    })
    db.session.commit()
    origin = request.environ['HTTP_REFERER']
    return redirect(origin)


@app.route("/class/add", methods=["GET"])
def add_class():
    if not session or not session["is_admin"]:
        abort(401)
    return render_template("add_class.html")


@app.route("/class/create", methods=["POST"])
def create_class():
    classname = request.form["classname"]
    description = request.form["description"]
    sql = text("INSERT INTO classes VALUES (:classname, :description)")
    db.session.execute(sql, {
        "classname": classname, "description": description
    })
    db.session.commit()
    flash(classname + " luotiin onnistuneesti")
    return redirect(url_for("add_class"))


@app.route("/myclasses")
def my_classes():
    if not session:
        abort(401)
    username = session["username"]
    sql = text("SELECT class FROM enrollments WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    enrollments = result.fetchall()
    return render_template("myclasses.html", enrollments=enrollments)


@app.context_processor
def utility_processor():
    def encode_url(string):
        safe_string = urllib.parse.quote_plus(string)
        return safe_string
    return dict(encode_url=encode_url)
