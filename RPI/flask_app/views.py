from flask import Blueprint, render_template

from flask_app.db import query_db

views = Blueprint("views", __name__)
@views.route("/")
def index():

    data = query_db(
        "SELECT *, "
        "max(time_updated) AS 'fill_updated [timestamp]'"
        "FROM fill_level "
        "NATURAL JOIN bin "
        "GROUP BY bin_name"
    )
    return render_template("index.html", data=data)

@views.route("/bin/<name>")
def bin_page(name):

    data = query_db(
        "SELECT *, "
        "max(time_updated) AS 'fill_updated [timestamp]'"
        "FROM fill_level "
        "NATURAL JOIN bin "
        "WHERE bin_name = ?",
        [name],
        True,
    )
    return render_template("/bin/index.html", data=data)

@views.route("/floorplan")
def floorplan():
    return render_template("/floorplan.html")
