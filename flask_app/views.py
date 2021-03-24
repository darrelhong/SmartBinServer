from flask import Blueprint, render_template

from flask_app.db import query_db

views = Blueprint('views', __name__)


@views.route('/')
def index():

    data = query_db("SELECT *, "
                    "max(time_updated) AS 'fill_updated [timestamp]'"
                    "FROM fill_level "
                    "NATURAL JOIN bin "
                    "GROUP BY bin_name")
    return render_template('index.html', data=data)
