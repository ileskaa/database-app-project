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
    classname = urllib.parse.unquote_plus(name)
    sql = text("SELECT description from classes WHERE name=:classname")
    result = db.session.execute(sql, {"classname": classname})
    single_row = result.fetchone()
    description = single_row.description
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




@app.context_processor
def utility_processor():
    def encode_url(string):
        safe_string = urllib.parse.quote_plus(string)
        return safe_string
    return dict(encode_url=encode_url)
