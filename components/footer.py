from dash import html


class Footer(html.Footer):

    def __init__(self):
        super().__init__(
            children=[
                html.P(
                    'Note: The CSV file should have columns for time/x-axis and signal values. \
                    The application will use the first column as x-axis data and the second column as signal data.',
                    className='text-muted')
            ],
            className='app-footer')
