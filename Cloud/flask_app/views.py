from datetime import date
from flask import Blueprint, render_template, Response, request
from jinja2.utils import consume

from flask_app.db import query_db

from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.dates import ConciseDateFormatter, AutoDateLocator
from matplotlib.backends.backend_svg import FigureCanvasSVG

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
    date_range = request.args.get("date_range") or "2"

    data = query_db(
        "SELECT *, "
        "max(time_updated) AS 'fill_updated [timestamp]'"
        "FROM fill_level "
        "NATURAL JOIN bin "
        "WHERE bin_name = ?",
        [name],
        True,
    )

    fill_history_2days = query_db(
        "SELECT * FROM fill_level WHERE "
        "bin_name = ? "
        "AND time_updated > datetime('now', '-2 days') "
        "ORDER BY time_updated ASC",
        [name],
    )

    exceed_70 = []

    for i in range(1, len(fill_history_2days)):
        if (
            fill_history_2days[i]["fill_percent"] >= 70
            and fill_history_2days[i - 1]["fill_percent"] < 70
        ):
            exceed_70.append(dict(fill_history_2days[i]))

    return render_template(
        "/bin/index.html",
        data=data,
        bin_name=name,
        exceed_70=exceed_70,
        date_range=date_range,
    )


@views.route("/floorplan")
def floorplan():
    data = query_db(
        "SELECT *, "
        "max(time_updated) AS time_updated "
        "FROM fill_level GROUP BY bin_name"
    )
    data = {x["bin_name"]: x["fill_percent"] for x in data}

    return render_template("/floorplan.html", data=data)


@views.route("/fill-chart/<name>/<date_range>")
def fill_chart(name, date_range):
    query = "SELECT bin_name, time_updated, fill_percent FROM bin NATURAL JOIN fill_level WHERE bin_name = ?"

    if date_range == "2":
        query += " AND time_updated > datetime('now', '-2 days')"

    data = query_db(query, [name])

    x = [row["time_updated"] for row in data]
    y = [row["fill_percent"] for row in data]

    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)

    # hide top and right axis
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    # HACKY WARNING show date as chart tiile
    # ax.set_title(data[0]["time_updated"].strftime("%A, %d %b %Y"), fontsize="medium")

    ax.set_ylabel("Fiil percent")
    ax.set_ylim([0, 100])

    # x axis interval and format
    locator = AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(ConciseDateFormatter(locator))
    fig.autofmt_xdate()

    # plot data
    ax.plot_date(x, y, "-")

    # Save it to a temporary buffer.
    output = BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    # Embed the result in the html output.
    return Response(output.getvalue(), mimetype="image/svg+xml")
