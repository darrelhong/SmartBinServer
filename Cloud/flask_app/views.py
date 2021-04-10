from flask import Blueprint, render_template, Response

from flask_app.db import query_db

from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter, MinuteLocator
from matplotlib.backends.backend_svg import FigureCanvasSVG

views = Blueprint('views', __name__)

@views.route('/')
def index():

    data = query_db("SELECT *, "
                    "max(time_updated) AS 'fill_updated [timestamp]'"
                    "FROM fill_level "
                    "NATURAL JOIN bin "
                    "GROUP BY bin_name")
    return render_template('index.html', data=data)


@views.route('/bin/<name>')
def bin_page(name):

    data = query_db("SELECT *, "
                    "max(time_updated) AS 'fill_updated [timestamp]'"
                    "FROM fill_level "
                    "NATURAL JOIN bin "
                    "WHERE bin_name = ?", [name], True)
    return render_template('/bin/index.html', data=data, bin_name=name)


@views.route('/floorplan')
def floorplan():
    return render_template('/floorplan.html')


@views.route("/fill-chart/<name>")
def fill_chart(name):
    data = query_db(
        "SELECT bin_name, time_updated, fill_percent FROM bin NATURAL JOIN fill_level WHERE bin_name = ?",
        [name],
    )
    x = [row["time_updated"] for row in data]
    y = [row["fill_percent"] for row in data]

    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)

    # hide top and right axis
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # HACKY WARNING show date as chart tiile
    ax.set_title(data[0]["time_updated"].strftime("%A, %d %b %Y"), fontsize="medium")

    ax.set_ylabel("Fiil percent")
    ax.set_ylim([0, 100])
    
    # x axis interval and format
    ax.xaxis.set_major_locator(MinuteLocator(interval=1))
    ax.xaxis.set_major_formatter(DateFormatter("%I:%M:%S %P"))
    fig.autofmt_xdate()

    # plot data
    ax.plot_date(x, y, "-")

    # Save it to a temporary buffer.
    output = BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    # Embed the result in the html output.
    return Response(output.getvalue(), mimetype="image/svg+xml")
