from flask import request, Blueprint, jsonify

from flask_app.db import query_db, get_db

# 200cm for now, to update accordingly
BIN_HEIGHT = 200

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


@api.route('/bin/update', methods=['POST'])
def update_bin():
    data = request.get_json()
    current = query_db('SELECT * FROM bin WHERE name = ?',
                       [data['microbit_name']], True)

    name = data['microbit_name']
    fill_percent = int(data['distance'] / BIN_HEIGHT * 100)
    cur = get_db().cursor()
    if current:
        cur.execute('UPDATE bin SET fill_percent = ? WHERE name = ?',
                    [fill_percent, name])
    else:
        cur.execute('INSERT INTO bin (name, fill_percent) VALUES (?, ?)', [
                    name, fill_percent])
    get_db().commit()

    return 'Success'
