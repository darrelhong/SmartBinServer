from flask import Blueprint, jsonify

from flask_app.db import query_db

# all routes are prefixed with /api
api = Blueprint('api', __name__)


@api.route('/')
def hello():
    return 'Hello API'


@api.route('/test')
def test():
    data = query_db('SELECT * FROM bin')
    result = [dict(item) for item in data]
    return jsonify(result)
