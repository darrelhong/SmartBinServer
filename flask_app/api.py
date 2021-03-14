from flask import Blueprint, jsonify

from flask_app.db import query_db

# all routes are prefixed with /api
api = Blueprint('api', __name__)


@api.route('/')
def hello():
    return 'Hello API'


@api.route('/bin/all')
def all():
    data = query_db('SELECT * FROM bin')
    result = [dict(item) for item in data]
    return jsonify(result)


@api.route('/bin/<name>')
def get_bin(name):
    data = query_db('SELECT * FROM bin WHERE name = ?', [name], True)
    if data:
        return jsonify(dict(data))
    return 'Bin not found', 400
