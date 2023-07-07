# web app
from dash import callback, no_update, dcc
from dash.dependencies import Input, Output


@callback(
    Output('notifications-container', 'children', allow_duplicate=True),
    Input('button-restart', 'n_clicks'),
    prevent_initial_call=True
)
def w(n_clicks):
    """This callback resets the app to its initial state when the start over button is clicked."""
    if n_clicks is not None:
        return dcc.Location(id='redirect', pathname='/setup', refresh=True)
    else:
        return no_update
