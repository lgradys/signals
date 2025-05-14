from enum import Enum

import dash_bootstrap_components as dbc
import numpy as np
from dash import dcc, html, Dash, Output, Input, State
from scipy import signal

from components.dropdown import Dropdown, Option
from components.signal_plot import SignalPlot
from components.signal_stats import SignalStats
from models.data import LoadedSignalData, FilteredSignalData
from models.figure import SignalFigure
from utils import figure, string, style


class FilterType(Enum):
    LOWPASS = 'Low pass'
    HIGHPASS = 'High pass'
    BANDPASS = 'Band pass'
    BANDSTOP = 'Band stop'


class SignalFiltering(dbc.Card):

    def __init__(self):
        super().__init__(
            id='signal-filtering',
            style=style.display_none(),
            children=[
                dbc.CardHeader('Signal Filtering'),
                dbc.CardBody(
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        html.Label('Filter Type:'),
                                        Dropdown(
                                            dropdown_id='filter-type',
                                            options=[Option(filterType.value, filterType.name) for filterType in
                                                     list(FilterType)],
                                            value=FilterType.LOWPASS.name)
                                    ],
                                    width=12, md=3),
                                dbc.Col(
                                    children=[
                                        html.Div(
                                            id='cutoff-container',
                                            children=[
                                                html.Label('Cutoff Frequency (Hz):'),
                                                dcc.Input(
                                                    id='cutoff-freq',
                                                    type='number',
                                                    min=0.01,
                                                    value=0.1,
                                                    className='form-control')
                                            ])
                                    ],
                                    width=12, md=3),
                                dbc.Col(
                                    children=[
                                        html.Div(
                                            id='cutoff-range-container',
                                            style=style.display_none(),
                                            children=[
                                                html.Label('Upper Cutoff Frequency (Hz):'),
                                                dcc.Input(
                                                    id='cutoff-freq-range',
                                                    type='number',
                                                    min=0.01,
                                                    value=10.0,
                                                    className='form-control')
                                            ])
                                    ],
                                    width=12, md=3),

                                # Filter order
                                dbc.Col(
                                    children=[
                                        html.Label('Filter Order:'),
                                        Dropdown(
                                            dropdown_id='filter-order',
                                            options=[Option(i, i) for i in range(0, 21)],
                                            value=4)
                                    ],
                                    width=12, md=3)
                            ],
                            className='mb-3'),

                        dbc.Button(
                            'Apply Filter',
                            id='apply-filter',
                            color='primary',
                            className='apply-button mb-3'),

                        SignalPlot(plot_id='filtered-signal')
                    ])
            ],
            className='app-card')

    def register_callbacks(self, app: Dash) -> 'SignalFiltering':
        @app.callback(
            Output('cutoff-container', 'children'),
            [Input('filter-type', 'value')])
        def update_cutoff_label(filter_type):
            return self.__update_cutoff_label(filter_type)

        @app.callback(
            Output('cutoff-range-container', 'style'),
            [Input('filter-type', 'value')])
        def toggle_cutoff_range_input(filter_type):
            return self.__toggle_cutoff_range_input(filter_type)

        @app.callback(
            [Output('filtered-signal-graph', 'figure'),
             Output('filtered-signal-stats', 'children'),
             Output('filtered-signal-plot', 'style')],
            [Input('apply-filter', 'n_clicks')],
            [State('original-signal-data', 'data'),
             State('filter-type', 'value'),
             State('cutoff-freq', 'value'),
             State('cutoff-freq-range', 'value'),
             State('filter-order', 'value')])
        def apply_filter(n_clicks, data, filter_type, cutoff_freq, cutoff_freq_range, filter_order):
            return self.__apply_filter(n_clicks, data, filter_type, cutoff_freq, cutoff_freq_range, filter_order)

        return self

    @staticmethod
    def __update_cutoff_label(filter_type):
        if filter_type in [FilterType.LOWPASS.name, FilterType.HIGHPASS.name]:
            label = 'Cutoff Frequency (Hz):'
        else:
            label = 'Lower Cutoff Frequency (Hz):'

        return [
            html.Label(label),
            dcc.Input(
                id='cutoff-freq',
                type='number',
                min=0.01,
                value=0.1,
                className='form-control')
        ]

    @staticmethod
    def __toggle_cutoff_range_input(filter_type):
        if filter_type in [FilterType.BANDPASS.name, FilterType.BANDSTOP.name]:
            return style.display_block()
        else:
            return style.display_none()

    def __apply_filter(self, n_clicks, data, filter_type, cutoff_freq, cutoff_freq_range, filter_order):
        if not n_clicks or not data:
            return figure.empty('No data loaded yet!'), string.empty(), style.display_none()

        try:
            loaded_signal_data = LoadedSignalData(**data)

            filtered_signal = self.__filter(cutoff_freq, cutoff_freq_range, filter_order, filter_type,
                                            loaded_signal_data)
            filtered_signal_data = FilteredSignalData(x_data=loaded_signal_data.x_data, y_data=filtered_signal,
                                                      x_label=loaded_signal_data.x_label,
                                                      y_label=loaded_signal_data.y_label, filter_type=filter_type,
                                                      cutoff_freq=cutoff_freq,
                                                      cutoff_freq_range=cutoff_freq_range, filter_order=filter_order)
            filtered_stats_component = SignalStats.create_stats_component(filtered_signal_data.calculate_stats())

            fig = self.__set_up_figure(loaded_signal_data, filtered_signal_data)

            return fig.figure, filtered_stats_component, style.display_block()

        except Exception as e:
            error_fig = figure.empty(f'Error applying filter: {str(e)}')
            return error_fig, html.P(f'Error: {str(e)}', style=style.color('red')), style.display_block()

    @staticmethod
    def __set_up_figure(loaded_signal_data: LoadedSignalData, filtered_signal_data: FilteredSignalData):
        fig = SignalFigure(rows=2, cols=1, subplot_titles=['Time Domain Comparison', 'Frequency Domain Comparison'])

        fig.add_trace(x_data=loaded_signal_data.x_data, y_data=loaded_signal_data.y_data, name='Original Signal',
                      color='blue', row=1, col=1)
        fig.add_trace(x_data=loaded_signal_data.x_data, y_data=filtered_signal_data.y_data, name='Filtered Signal',
                      color='green', row=1, col=1)
        fig.add_trace(x_data=loaded_signal_data.spectral_analyze_result.fft_freq,
                      y_data=loaded_signal_data.spectral_analyze_result.fft_magnitude, name='Original Spectrum',
                      color='blue',
                      row=2, col=1)
        fig.add_trace(x_data=filtered_signal_data.spectral_analyze_result.fft_freq,
                      y_data=filtered_signal_data.spectral_analyze_result.fft_magnitude, name='Filtered Spectrum',
                      color='green', row=2, col=1)

        fig.update_x_axis(title=loaded_signal_data.x_label, row=1, col=1)
        fig.update_x_axis(title='Frequency (Hz)', row=2, col=1)
        fig.update_y_axis(title=loaded_signal_data.y_label, title_standoff=25, row=1, col=1)
        fig.update_y_axis(title='Magnitude', title_standoff=25, row=2, col=1)

        return fig

    @staticmethod
    def __filter(cutoff_freq, cutoff_freq_range, filter_order, filter_type, loaded_signal_data):
        if len(loaded_signal_data.x_data) > 1:
            fs = 1.0 / np.mean(np.diff(loaded_signal_data.x_data)).astype(float)
        else:
            fs = 1.0

        nyquist = 0.5 * fs
        if filter_type in [FilterType.LOWPASS.name, FilterType.HIGHPASS.name]:
            wn = cutoff_freq / nyquist
        else:
            wn = sorted([cutoff_freq / nyquist, cutoff_freq_range / nyquist])

        sos = signal.butter(filter_order, wn, btype=filter_type, output='sos')
        return signal.sosfilt(sos, loaded_signal_data.y_data)
