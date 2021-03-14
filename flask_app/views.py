from flask import Blueprint, render_template

from flask_app.db import query_db

views = Blueprint('views', __name__)


@views.route('/')
def index():
    data = query_db('SELECT * FROM bin')
    return render_template('index.html', data=data)
