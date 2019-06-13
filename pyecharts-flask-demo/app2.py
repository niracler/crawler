from random import randrange
from flask.json import jsonify
from flask import Flask, render_template
from pyecharts import options as opts
from pyecharts.charts import Line
import redis

app = Flask(__name__, static_folder="templates")


def line_base() -> Line:
    line = (
        Line()
        .add_xaxis(["{}".format(i) for i in range(10)])
        .add_yaxis(
            series_name="",
            y_axis=[randrange(50, 80) for _ in range(10)],
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="动态数据"),
            xaxis_opts=opts.AxisOpts(type_="value"),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
    )
    return line


@app.route("/")
def index():
    return render_template("index2.html")


@app.route("/lineChart")
def get_line_chart():
    c = line_base()
    return c.dump_options()


idx = 9


@app.route("/lineDynamicData")
def update_line_data():
    client = redis.Redis(host='10.42.31.236', port='6379', password='123456')
    num = client.llen("weibo_follow_redis:items")
    global idx
    idx = idx + 1
    return jsonify({"name": idx, "value": num})


if __name__ == "__main__":
    app.run()