import base64
import io
import os
from typing import Any

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html, Output, Input, Dash, State
from pandas import DataFrame

from components.dropdown import Dropdown
from utils.string import empty
from utils.style import display_none, display_block, color


class FileSelector(dbc.Tab):

    def __init__(self, tab_id: str):
        super().__init__(
            label='Upload Data',
            tab_id=tab_id,
            children=[
                html.Div(
                    children=[
                        html.P('Upload a CSV file containing signal data:', className='mt-3'),
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select a CSV File')
                            ]),
                            className='upload-area',
                            multiple=False),
                    ]),
            ])


class ExampleSelector(dbc.Tab):

    def __init__(self, tab_id: str):
        super().__init__(
            label='Example Signals',
            tab_id=tab_id,
            children=[
                html.Div(
                    children=[
                        html.P('Select an example signal:', className='mt-3'),
                        Dropdown(dropdown_id='example-dropdown', options=[]),
                    ]),
            ])


class DataSource(dbc.Card):

    def __init__(self):
        self.__upload_tab = 'upload-tab'
        self.__example_tab = 'example-tab'
        self.__active_tab = self.__upload_tab
        super().__init__(
            children=[
                dbc.CardHeader('Data Source Selection'),
                dbc.CardBody(
                    children=[
                        dbc.Tabs(
                            children=[FileSelector(self.__upload_tab), ExampleSelector(self.__example_tab)],
                            id='data-source-tabs',
                            active_tab=self.__active_tab),
                        html.Div(id='upload-output', className='mt-3')
                    ])
            ], className='app-card mb-4')

    def register_callbacks(self, app: Dash) -> 'DataSource':

        @app.callback(
            Output('example-dropdown', 'options'),
            Input('data-source-tabs', 'active_tab'))
        def handle_active_tab(active_tab: str) -> list[dict[str, str]]:
            self.__update_active_tab(active_tab)
            return self.__get_examples(active_tab)

        @app.callback(
            [Output('raw-signal-data', 'data'),
             Output('upload-output', 'children'),
             Output('raw-signal-plot', 'style'),
             Output('signal-filtering', 'style')],
            [Input('upload-data', 'contents'),
             Input('example-dropdown', 'value')],
            [State('upload-data', 'filename'),
             State('data-source-tabs', 'active_tab')])
        def process_data(upload_contents, example_filename, upload_filename, active_tab):
            return self.__process_data(upload_contents, example_filename, upload_filename, active_tab)

        return self

    def __update_active_tab(self, active_tab):
        self.__active_tab = active_tab

    def __get_examples(self, active_tab: str) -> list[dict[str, str]]:
        examples = os.path.join(os.getcwd(), 'assets/examples')
        if not os.path.exists(examples) or active_tab != self.__example_tab:
            return []
        return [{'label': file, 'value': file} for file in os.listdir(examples) if file.endswith('.csv')]

    def __process_data(self, upload_contents, example_filename, upload_filename, active_tab):
        try:
            if active_tab == self.__upload_tab and upload_contents:
                df, filename = self.__load_data_from_file(upload_contents, upload_filename)

            elif active_tab == self.__example_tab and example_filename:
                df, filename = self.__load_data_from_example(example_filename)
            else:
                return {}, empty(), display_none(), display_none()

            if len(df.columns) >= 2:
                data = self.__extract_data(df, filename)

                return data, html.Div(
                    children=[
                        html.P(f'File {filename} loaded successfully!'),
                        html.P(f'Data shape: {df.shape[0]} rows, {df.shape[1]} columns'),
                        html.P(f'Columns: {", ".join(df.columns)}')
                    ]), display_block(), display_block()
            else:
                return {}, html.Div(
                    children=[
                        html.P('The CSV file must have at least two columns:'),
                        html.P('1. X-axis data (e.g., time)'),
                        html.P('2. Signal data')
                    ],
                    style=color('red')), display_none(), display_none()

        except Exception as e:
            return {}, html.Div(
                children=[
                    html.P(f'An error occurred: {str(e)}')
                ],
                style=color('red')), display_none(), display_none()

    @staticmethod
    def __extract_data(df: DataFrame, filename: str) -> dict[str, Any]:
        return {
            'filename': filename,
            'x_data': df.iloc[:, 0],
            'y_data': df.iloc[:, 1],
            'x_label': df.columns[0],
            'y_label': df.columns[1],
            'shape': (df.shape[0], df.shape[1]),
            'columns': df.columns
        }

    @staticmethod
    def __load_data_from_file(upload_contents, upload_filename) -> tuple[DataFrame, str]:
        content_type, content_string = upload_contents.split(',')
        decoded = base64.b64decode(content_string)
        return pd.read_csv(io.StringIO(decoded.decode('utf-8'))), upload_filename

    @staticmethod
    def __load_data_from_example(example_filename) -> tuple[DataFrame, str]:
        examples = os.path.join(os.getcwd(), 'assets/examples')
        file_path = os.path.join(examples, example_filename)
        return pd.read_csv(file_path), example_filename
