# web app
from dash import callback, MATCH, ALL
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# local packages
import src


@callback(
    Output({'type': 'menu-user', 'index': ALL}, 'style'),
    Input('location', 'pathname'),
    Input('user-config', 'data'),
)
def change_menu_visibility(pathname, user):
    if pathname != '/login' and user is not None:
        style = None
        return style, style, style
    style = {'display': 'none'}
    return style, style, style


@callback(
    Output({'type': 'modal', 'index': MATCH}, 'opened', allow_duplicate=True),
    Input({'type': 'menu-user', 'index': MATCH}, 'n_clicks'),
    prevent_initial_call=True
)
def open_modal_menu_user(n_clicks):
    is_open = n_clicks is not None
    return is_open


@callback(
    Output({'type': 'modal', 'index': MATCH}, 'opened', allow_duplicate=True),
    Input({'type': 'menu-community', 'index': MATCH}, 'n_clicks'),
    prevent_initial_call=True,
)
def open_modal_menu_community(n_clicks):
    is_open = n_clicks is not None
    return is_open


@callback(
    {
        'rings': [Output({'type': 'ring', 'index': iso}, 'sections') for iso in src.utils.get_language_mapping()],
        'user-count': Output('user-count', 'children'),
    },
    Input('interval-component', 'n_intervals'),
)
def update_stats(_: int):
    stats = src.database.get_stats_by_language()
    output = dict()
    output['rings'] = [[{'value': stats.get(iso, 0), 'color': src.ui.styles.PRIMARY_COLOUR}] for iso in src.utils.get_language_mapping()]
    count = src.database.get_user_count()
    output['user-count'] = src.ui.extras.insert_user_count(count)
    return output


@callback(
    Output({'type': 'modal', 'index': 'statistics'}, 'children'),
    Input('interval-component', 'n_intervals'),
    State('user-config', 'data'),
)
def update_user_stats(_: int, user: dict):
    if user is None:
        raise PreventUpdate
    n_labels = src.database.get_stats_user(user['_id'])
    user_stats = src.ui.extras.insert_user_stats(n_labels)
    return user_stats
