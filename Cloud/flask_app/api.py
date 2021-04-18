from flask import request, Blueprint, jsonify
import sqlite3

from flask_app.db import query_db, get_db

# 200cm for now, to update accordingly
BIN_HEIGHT = 200

# all routes are prefixed with /api
api = Blueprint("api", __name__)
@api.route("/")
def hello():
    return "Hello API"

@api.route("/fill-level/all")
def all_fill_level():
    data = query_db("SELECT * FROM bin NATURAL JOIN fill_level")
    result = [dict(item) for item in data]
    return jsonify(result)

@api.route("/fill-level/latest")
def latest_fill_level():
    data = query_db(
        "SELECT *, "
        "max(time_updated) AS time_updated "
        "FROM fill_level GROUP BY bin_name"
    )
    result = [dict(item) for item in data]
    return jsonify(result)

@api.route("/fill-level/name/<name>")
def bin_fill_level(name):
    data = query_db(
        "SELECT * FROM bin NATURAL JOIN fill_level WHERE bin_name = ?", [name]
    )
    if data:
        return jsonify([dict(item) for item in data])
    return "Bin not found", 400

@api.route("/fill-level/latest/<name>")
def bin_latest_fill_level(name):
    data = query_db(
        "SELECT * FROM bin NATURAL JOIN fill_level "
        "WHERE bin_name = ? "
        "ORDER BY time_updated DESC "
        "LIMIT 1",
        [name],
        True,
    )
    if data:
        return jsonify(dict(data))
    return "Bin not found", 400

@api.route("/fill-level/update", methods=["POST"])
def update_bin():
    data = request.get_json()
    name = data["bin_name"]
    current = query_db("SELECT * FROM bin WHERE bin_name = ?", [name], True)
    if current:
        if data["distance"] <= BIN_HEIGHT:
            fill_percent = int(data["distance"] / BIN_HEIGHT * 100)
            cur = get_db().cursor()
            cur.execute(
                "INSERT INTO fill_level (fill_percent, time_updated, bin_name) VALUES " "(?, datetime('now', 'localtime'), ?)",
                [fill_percent, name],
            )
            get_db().commit()
            return "Success"
        return "Bin height exceeded", 400
    return "Bin not found", 400

@api.route("/spill/update", methods=["POST"])
def update_spill():
    data = request.get_json()
    name = data["bin_name"]
    current = query_db("SELECT * FROM bin WHERE bin_name = ?", [name], True)
    if current:
        try:
            cur = get_db().cursor()
            cur.execute(
                "UPDATE bin set is_spill = ? WHERE bin_name = ?",
                [data["spill_status"], name],
            )
            get_db().commit()
            return "Success"
        except sqlite3.IntegrityError:
            return "Invalid status", 400
    return "Bin not found", 400

@api.route("/tilt/update", methods=["POST"])
def update_tilt():
    data = request.get_json()
    name = data["bin_name"]
    current = query_db("SELECT * FROM bin WHERE bin_name = ?", [name], True)
    if current:
        try:
            cur = get_db().cursor()
            cur.execute(
                "UPDATE bin set is_tilt = ? WHERE bin_name = ?",
                [data["tilt_status"], name],
            )
            get_db().commit()
            return "Success"
        except sqlite3.IntegrityError:
            return "Invalid status", 400
    return "Bin not found", 400
