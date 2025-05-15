import dash_bootstrap_components as dbc
from dash import dcc, html, Dash, Output, Input

from components.signal_stats import SignalStats
from models.data import LoadedSignalData
from models.figure import SignalFigure
from utils import figure
from utils.style import display_none


class SignalPlot(dbc.Card):

    def __init__(self, plot_id: str):
        plot_name = plot_id.replace('-', ' ').title()
        self.__stats = SignalStats(stats_id=f'{plot_id}-stats')
        super().__init__(
            id=f'{plot_id}-plot',
            style=display_none(),
            children=[
                dbc.CardHeader(f'{plot_name}'),
                dbc.CardBody(
                    children=[
                        dcc.Loading(
                            id=f'{plot_id}-loading-graph',
                            type='circle',
                            children=html.Div(
                                children=[
                                    dcc.Graph(
                                        id=f'{plot_id}-graph',
                                        figure={},
                                        className='graph-container')
                                ])),
                        self.__stats
                    ])
            ],
            className='app-card mb-4')

    def register_callbacks(self, app: Dash) -> 'SignalPlot':
        @app.callback(
            [Output('raw-signal-graph', 'figure'),
             Output('raw-signal-stats', 'children')],
            Input('raw-signal-data', 'data'))
        def update_graph(data):
            return self.__update_graph(data)

        return self

    def __update_graph(self, data: dict[str, list[float]]):
        if not data:
            return figure.empty('No data uploaded'), None

        signal_data = LoadedSignalData(**data)
        stats_component = self.__stats.create_stats_component(signal_data.calculate_stats())

        fig = self.__set_up_figure(signal_data)

        return fig.figure, stats_component

    @staticmethod
    def __set_up_figure(signal_data) -> SignalFigure:
        fig = SignalFigure(rows=2, cols=1, subplot_titles=['Time Domain', 'Frequency Domain'])

        fig.add_trace(x_data=signal_data.x_data, y_data=signal_data.y_data, color='blue', row=1, col=1)
        fig.add_trace(x_data=signal_data.spectral_analyze_result.fft_freq,
                      y_data=signal_data.spectral_analyze_result.fft_magnitude, color='green', row=2, col=1)

        fig.update_x_axis(title=signal_data.x_label, row=1, col=1)
        fig.update_x_axis(title='Frequency (Hz)', row=2, col=1)
        fig.update_y_axis(title=signal_data.y_label, title_standoff=25, row=1, col=1)
        fig.update_y_axis(title='Magnitude', title_standoff=25, row=2, col=1)

        return fig
