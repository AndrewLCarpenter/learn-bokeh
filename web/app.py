from flask import Flask, render_template
from bokeh.embed import components, autoload_server
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from plot_server.server_instance import BokehManager

from functools import lru_cache
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return 'hah'

@app.route('/hello-world')
def hello_world():
    # init a basic bar chart:
    fig = figure(plot_width=600, plot_height=600)
    fig.vbar(
        x=[1, 2, 3, 4],
        width=0.5,
        bottom=0,
        top=[1.7, 2.2, 4.6, 3.9],
        color='navy'
    )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)

# bok = BokehManager('/home/andrew/projects/learn-bokeh/web/plot_server/doit.py')
# bok.start_bokeh()
@app.route('/stock-plot')
def stock_plot():
    from plot_server.doit import script
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    # script = autoload_server(url='http://localhost:5006/doit')
    import pprint
    pprint.pprint(script)
    html = render_template('index.html',
                           plot_script=script,
                           js_resources=js_resources,
                           css_resources=css_resources,
                           )
    return encode_utf8(html)

if __name__ == '__main__':
    app.run(debug=True)