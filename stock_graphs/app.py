from flask import Flask
# Plotly and Dash import
import chart_studio.plotly as py
import plotly.graph_objs as go
import chart_studio
chart_studio.tools.set_credentials_file(username='group13Yes', api_key='OspkIgNNW6CTIM7110px')

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"
