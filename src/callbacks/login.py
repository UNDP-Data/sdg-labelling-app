# web app
from dash import callback, dcc, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# local packages
import src


@callback(
    Output('login-redirect', 'children'),
    Input('location', 'pathname'),
    Input('user-config', 'data'),
    Input('session-config', 'data'),
)
def redirect(pathname, user, config):
    if pathname != '/login' and user is None:
        return dcc.Location(id='redirect', pathname='/login', refresh=True)
    elif pathname == '/login' and user is not None:
        return dcc.Location(id='redirect', pathname='/setup', refresh=True)
    elif pathname == '/labelling' and config is None:
        return dcc.Location(id='redirect', pathname='/setup', refresh=True)
    else:
        raise PreventUpdate


@callback(
    Output('user-config', 'data'),
    Output('email-input', 'error'),
    Output('code-input', 'error'),
    Input('button-login', 'n_clicks'),
    State('email-input', 'value'),
    State('code-input', 'value'),
    prevent_initial_call=True
)
def login(n_clicks, email, access_code):
    if not n_clicks:
        raise PreventUpdate
    is_valid_email = src.utils.validate_email(email=email)
    user = src.database.get_user(email=email, access_code=access_code)
    if not is_valid_email:
        return no_update, 'Invalid email address', no_update
    elif user is None:
        return no_update, None, 'Invalid access code'
    else:
        return user, None, None


@callback(
    Output('leaderboard', 'children'),
    Input('interval-component', 'n_intervals'),
)
def update_leaderboard(_: int):
    users = src.utils.create_leaderboard_entries(src.database.get_top_annotators(limit=50))
    leaderboard = src.ui.tables.create_table(users)
    return leaderboard


@callback(
    Output('email-button', 'disabled', allow_duplicate=True),
    Output('start-button', 'disabled', allow_duplicate=True),
    Output('notifications-container', 'children', allow_duplicate=True),
    Input('email-button', 'disabled'),
    State('email-input', 'value'),
    prevent_initial_call=True,
)
def send_access_code(_, email):
    if not email:
        raise PreventUpdate
    access_code = src.communication.send_access_code(email=email)
    if access_code is None:
        notification = src.ui.notifications.get_notification_failed(email=email)
        is_disabled = False
    else:
        src.database.upsert_user_code(email=email, access_code=access_code)
        notification = src.ui.notifications.get_notification_sent(email=email)
        is_disabled = True
    return is_disabled, False, notification


@callback(
    Output('email-input', 'error', allow_duplicate=True),
    Output('email-button', 'disabled', allow_duplicate=True),
    Output('start-button', 'disabled', allow_duplicate=True),
    Output('notifications-container', 'children', allow_duplicate=True),
    Input('email-button', 'n_clicks'),
    State('email-input', 'value'),
    prevent_initial_call=True,
)
def disable_buttons_while_sending(n_clicks, email):
    if not n_clicks:
        raise PreventUpdate
    elif not src.utils.validate_email(email=email):
        error_message = 'Please, provide a valid email address for your organisation.'
        return error_message, no_update, no_update, no_update
    notification = src.ui.notifications.get_notification_sending(email=email)
    is_disabled = True
    error_message = None
    return error_message, is_disabled, is_disabled, notification
