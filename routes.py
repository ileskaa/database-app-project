from db import db
from app import app
from flask import (
    render_template, request, redirect, session, abort, flash, url_for
)
from sqlalchemy.sql import text
import urllib.parse


def get_classes():
    sql = text("SELECT name FROM classes")
    result = db.session.execute(sql)
    classes = result.fetchall()
    return classes


@app.route("/")
def index():
    if session and "username" in session:
        username = session['username']
        sql = text("SELECT admin FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        is_admin = result.fetchone().admin
        return render_template(
            "index.html", classes=get_classes(), is_admin=is_admin
        )
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


def get_class_description(classname: str):
    sql_get_description = text(
        "SELECT description from classes WHERE name=:classname"
    )
    result = db.session.execute(sql_get_description, {"classname": classname})
    single_row = result.fetchone()
    return single_row.description


def check_if_registered(classname: str):
    sql_count = text("SELECT COUNT(*) FROM enrollments \
        WHERE username=:username AND class=:classname")
    username = session["username"]
    result = db.session.execute(sql_count, {
        "username": username,
        "classname": classname
    })
    single_row = result.fetchone()
    is_registered = single_row.count
    return is_registered


def get_comments(classname: str):
    sql_get_comments = text(
        "SELECT id, username, comment from comments WHERE classname=:classname"
    )
    result = db.session.execute(sql_get_comments, {
        "classname": classname
    })
    comment_rows = result.fetchall()
    return comment_rows


def get_enrolled_members(classname: str):
    "SELECT id, fname, lname, username FROM members JOIN users ON id=member_id"
    sql = text(
        "SELECT enrollments.username, fname, lname FROM enrollments \
            JOIN users ON enrollments.username=users.username \
            JOIN members ON id=member_id WHERE class=:classname"
    )
    result = db.session.execute(sql, {
        "classname": classname
    })
    rows = result.fetchall()
    return rows


# You can put variable names in your view functions
@app.route("/class/<name>")
def classes(name):
    if not session:
        abort(401)
    classname = urllib.parse.unquote_plus(name)
    if session["is_admin"]:
        print(get_enrolled_members(classname))
        return render_template(
            "class.html",
            classname=classname,
            description=get_class_description(classname),
            comment_rows=get_comments(classname),
            enrolled_members=get_enrolled_members(classname)
        )
    return render_template(
        "class.html",
        classname=classname,
        description=get_class_description(classname),
        is_registered=check_if_registered(classname),
        comment_rows=get_comments(classname)
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


@app.route("/class/remove", methods=["POST"])
def remove_class():
    classname = request.form["classname"]
    sql = text("DELETE FROM classes WHERE name=:classname")
    db.session.execute(sql, {
        "classname": classname
    })
    db.session.commit()
    flash(classname + " poistettiin")
    return redirect(url_for("index"))


@app.route("/class/comment", methods=["POST"])
def send_comment():
    classname = request.form["class"]
    username = session["username"]
    comment = request.form["comment"]
    sql = text(
        "INSERT INTO comments(classname, username, comment) \
            VALUES (:classname, :username, :comment)"
    )
    db.session.execute(sql, {
        "classname": classname,
        "username": username,
        "comment": comment
    })
    db.session.commit()
    origin = request.environ['HTTP_REFERER']
    return redirect(origin)


@app.route("/myclasses")
def my_classes():
    if not session:
        abort(401)
    username = session["username"]
    sql = text("SELECT class FROM enrollments WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    enrollments = result.fetchall()
    return render_template("myclasses.html", enrollments=enrollments)


@app.route("/delete/comment", methods=["POST"])
def delete_comment():
    comment_id = request.form["comment_id"]
    sql = text("DELETE FROM comments WHERE id=:id")
    db.session.execute(sql, {"id": comment_id})
    db.session.commit()
    origin = request.environ['HTTP_REFERER']
    return redirect(origin)


@app.route("/members")
def members():
    if not session or not session["is_admin"]:
        abort(401)
    sql = text("SELECT id, fname, lname, email FROM members")
    result = db.session.execute(sql)
    members = result.fetchall()
    return render_template("members.html", members=members)


@app.route("/remove/member", methods=["POST"])
def remove_member():
    member_id = request.form["member_id"]
    sql = text("DELETE FROM members WHERE id=:id")
    db.session.execute(sql, {"id": member_id})
    db.session.commit()
    origin = request.environ['HTTP_REFERER']
    return redirect(origin)


@app.route("/remove/enrollment", methods=["POST"])
def remove_enrollment():
    username = request.form["username"]
    classname = request.form["classname"]
    sql = text(
        "DELETE FROM enrollments WHERE username=:username \
            AND class=:classname")
    db.session.execute(sql, {"username": username, "classname": classname})
    db.session.commit()
    origin = request.environ['HTTP_REFERER']
    return redirect(origin)


@app.context_processor
def utility_processor():
    def encode_url(string):
        safe_string = urllib.parse.quote_plus(string)
        return safe_string
    return dict(encode_url=encode_url)
