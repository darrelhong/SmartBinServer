from flask import request, Blueprint, jsonify

from flask_app.db import query_db, get_db

# 200cm for now, to update accordingly
BIN_HEIGHT = 200

# all routes are prefixed with /api
api = Blueprint('api', __name__)


@api.route('/')
def hello():
    return 'Hello API'


@api.route('/fill-level/all')
def all_fill_level():
    data = query_db("SELECT * FROM bin NATURAL JOIN fill_level")
    result = [dict(item) for item in data]
    return jsonify(result)


@api.route('/fill-level/latest')
def latest_fill_level():
    data = query_db("SELECT *, "
                    "max(time_updated) AS time_updated "
                    "FROM fill_level GROUP BY bin_name")
    result = [dict(item) for item in data]
    return jsonify(result)


@api.route('/fill-level/name/<name>')
def bin_fill_level(name):
    data = query_db(
        "SELECT * FROM bin NATURAL JOIN fill_level WHERE bin_name = ?",
        [name])
    if data:
        return jsonify([dict(item) for item in data])
    return 'Bin not found', 400


@api.route('/fill-level/latest/<name>')
def bin_latest_fill_level(name):
    data = query_db("SELECT * FROM bin NATURAL JOIN fill_level "
                    "WHERE bin_name = ? "
                    "ORDER BY time_updated DESC "
                    "LIMIT 1", [name], True)
    if data:
        return jsonify(dict(data))
    return 'Bin not found', 300


@api.route('/update/fill-level', methods=['POST'])
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
