from dash import html


class SignalStats(html.Div):

    def __init__(self, stats_id):
        super().__init__(id=stats_id, className='stats-table')

    @staticmethod
    def create_stats_component(stats: dict[str, float]):
        if not stats:
            return html.P('No data available')

        return html.Div(
            children=[
                html.Table(
                    children=[
                        html.Tbody(
                            children=[
                                html.Tr(
                                    children=[
                                        html.Td(name),
                                        html.Td(f'{value:.4g}')
                                    ])
                                for name, value in stats.items()
                            ])
                    ], className='table table-sm table-striped')
            ])
