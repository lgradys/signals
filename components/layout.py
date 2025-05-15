import dash_bootstrap_components as dbc
from dash import dcc, html, Dash

from components.datasource import DataSource
from components.footer import Footer
from components.signal_filtering import SignalFiltering
from components.signal_plot import SignalPlot


class Layout(dbc.Container):

    def __init__(self, app: Dash):
        super().__init__(
            children=[
                html.Div(
                    children=[
                        html.Hr(),
                        DataSource().register_callbacks(app),
                        html.Div(
                            children=[
                                SignalPlot(plot_id='raw-signal').register_callbacks(app),
                                SignalFiltering().register_callbacks(app)
                            ]),
                        Footer()],
                    className='dash-container'),

                dcc.Store(id='raw-signal-data')],
            fluid=True)
