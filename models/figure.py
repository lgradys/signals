import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class SignalFigure:

    def __init__(self, rows: int, cols: int, subplot_titles: list[str]):
        self.__fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=subplot_titles,
            shared_xaxes=False,
            vertical_spacing=0.25)
        self.__update_layout()

    def add_trace(self, x_data: np.array, y_data: np.array, color: str, row: int, col: int, show_legend: bool = False,
                  name: str = None):
        self.__fig.add_trace(
            go.Scatter(x=x_data, y=y_data, mode='lines', line=dict(color=color), showlegend=show_legend, name=name),
            row=row,
            col=col)

    def update_x_axis(self, title: str, row: int, col: int):
        self.__fig.update_xaxes(title_text=title, row=row, col=col)

    def update_y_axis(self, title: str, title_standoff: int, row: int, col: int):
        self.__fig.update_yaxes(title_text=title, title_standoff=title_standoff, row=row, col=col)

    @property
    def figure(self) -> go.Figure:
        return self.__fig

    def __update_layout(self):
        self.__fig.update_layout(
            height=800,
            template='plotly_dark',
            showlegend=True,
            legend=dict(
                orientation='v',
                yanchor='middle',
                y=0.5,
                xanchor='right',
                x=1.2))
