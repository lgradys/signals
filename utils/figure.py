import plotly.graph_objects as go

from utils import string


def empty(title: str) -> go.Figure:
    empty_fig = go.Figure()
    empty_fig.update_layout(
        title=title,
        xaxis=dict(title=string.empty()),
        yaxis=dict(title=string.empty()))
    return empty_fig
