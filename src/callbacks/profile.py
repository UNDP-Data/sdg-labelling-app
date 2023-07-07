# web app
from dash import callback, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# local packages
import src


@callback(
    Output('user-profile-id', 'children'),
    Output('user-profile-leaderboard', 'checked'),
    Output('user-profile-name', 'value'),
    Output('user-profile-team', 'value'),
    Input({'type': 'modal', 'index': 'profile'}, 'opened'),
    State('user-config', 'data'),
    prevent_initial_call=True
)
def populate_profile(_, user):
    return user['_id'], user.get('leaderboard', False), user.get('name'), user.get('team')


@callback(
    Output('user-profile-name', 'disabled'),
    Output('user-profile-team', 'disabled'),
    Input('user-profile-leaderboard', 'checked'),
    prevent_initial_call=True
)
def make_profile_editable(checked: bool):
    disabled = not checked
    return disabled, disabled


@callback(
    Output('user-config', 'data', allow_duplicate=True),
    Output('notifications-container', 'children', allow_duplicate=True),
    Output('button-save-profile', 'error'),
    Input('button-save-profile', 'n_clicks'),
    State('user-profile-leaderboard', 'checked'),
    State('user-profile-name', 'value'),
    State('user-profile-team', 'value'),
    State('user-config', 'data'),
    prevent_initial_call=True
)
def save_profile(n_clicks, user_leaderboard, user_name, user_team, user):
    if n_clicks is None:
        raise PreventUpdate

    user['leaderboard'] = user_leaderboard
    user['name'] = user_name
    user['team'] = user_team
    matched_count = src.database.update_user_profile(user)
    if not matched_count:
        return no_update, no_update, 'Unexpected error. Could not save the settings. Please, contact the developers.'
    notification = src.ui.notifications.get_notification_profile()
    return user, notification, None
