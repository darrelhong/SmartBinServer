from flask import Blueprint, render_template

from flask_app.db import query_db

views = Blueprint('views', __name__)


@views.route('/')
def index():

    data = query_db("SELECT *, "
                    "max(time_updated) AS time_updated "
                    "FROM fill_level GROUP BY bin_name")
    return render_template('index.html', data=data)
