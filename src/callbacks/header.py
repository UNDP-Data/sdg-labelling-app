# web app
from dash import callback, MATCH
from dash.dependencies import Input, Output

# local packages
import src


@callback(
    Output('modal-faq', 'opened'),
    Input('faq-button', 'n_clicks'),
    prevent_initial_call=True
)
def open_modal_faq(n_clicks):
    is_open = n_clicks is not None
    return is_open


@callback(
    Output({'type': 'modal', 'index': MATCH}, 'opened'),
    Input({'type': 'menu-user', 'index': MATCH}, 'n_clicks'),
    prevent_initial_call=True
)
def open_modal_menu(n_clicks):
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
