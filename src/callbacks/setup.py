# web app
from dash import callback, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# local packages
import src


@callback(
    Output('notifications-container', 'children', allow_duplicate=True),
    Output('session-config', 'data',  allow_duplicate=True),
    Input('start-button', 'n_clicks'),
    State('slider', 'value'),
    State('language-input', 'value'),
    State('user-config', 'data'),
    prevent_initial_call=True
)
def start_labelling(n_clicks, n_tasks, language, user):
    if not n_clicks:
        raise PreventUpdate
    config = src.entities.SessionConfig(
        task_idx=0,
        task_ids=[None] * n_tasks,
        user_id=user['_id'],
        language=language,
    )
    return dcc.Location(id='redirect', pathname='/labelling', refresh=True), config.dict()
