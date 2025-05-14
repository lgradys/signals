import dash
import dash_bootstrap_components as dbc

from components.layout import Layout
from utils.env import DEBUG

app = dash.Dash(
    name=__name__,
    external_stylesheets=[
        dbc.themes.DARKLY,
        'https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap'
    ],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}])
server = app.server

app.layout = Layout(app)

if __name__ == '__main__':
    app.run(debug=DEBUG)
