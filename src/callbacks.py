# dash
from dash import callback, callback_context, no_update, MATCH, ALL
from dash.dependencies import Input, Output, State

# local packages
from src import database, components, styles, utils


@callback(
    Output('content', 'children', allow_duplicate=True),
    Input('start-over-button', 'n_clicks'),
    prevent_initial_call=True
)
def start_over_button(n_clicks):
    """This callback resets the app to its initial state when the start over button is clicked."""
    if n_clicks is not None:
        return components.get_start_layout()
    else:
        return no_update


@callback(
    Output('content', 'children'),
    Output('modal', 'opened', allow_duplicate=True),
    Input('quit-modal-button', 'n_clicks'),
    State('modal', 'opened'),
    prevent_initial_call=True

)
def quit_app(n_clicks, is_open):
    """Quit the app and change the layout to the start layout."""
    ctx = callback_context
    if ctx.triggered_id == 'quit-modal-button' and n_clicks is not None:
        return components.get_finish_layout(reason='session_quit'), False
    else:
        return no_update, is_open


@callback(
    Output('content', 'children', allow_duplicate=True),
    Output('session-config', 'data',  allow_duplicate=True),
    Output('email-input', 'error'),
    Input('start-button', 'n_clicks'),
    State('slider', 'value'),
    State('language-input', 'value'),
    State('email-input', 'value'),
    prevent_initial_call=True
)
def change_to_main_layout(n_clicks, input_value, language, email):
    """Change start layout to main layout."""
    if utils.validate_email(email=email):
        config = {
            'IDX_CURRENT': -1,  # increases on load
            'SESSION_IDS': [None] * input_value,  # track doc ids the use has seen in this session
            'USER_LANGUAGE': language,
            'USER_EMAIL': email,
        }
        return components.get_main_layout(), config, no_update
    else:
        return no_update, no_update, 'Invalid email address'


@callback(
    Output('modal', 'opened', allow_duplicate=True),
    Input('quit-button', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_modal(n_clicks):
    """Toggle the modal."""
    return n_clicks is not None


@callback(
    Output('progress-bar', 'value'),
    Output('progress-bar', 'label'),
    Output('chip-container', 'children'),
    Output('paper', 'children'),
    Output('content', 'children', allow_duplicate=True),
    Output('session-config', 'data', allow_duplicate=True),
    Input('next-button', 'n_clicks'),
    Input('back-button', 'n_clicks'),
    State('session-config', 'data'),
    State({'type': 'sdg-button', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def update_components(n_clicks_next, n_clicks_back, config, n_clicks_sdgs):
    """Update the components of the main layout and the database with the current state of the labeling."""
    idx_current = config['IDX_CURRENT']
    session_ids = config['SESSION_IDS']
    email = config['USER_EMAIL']
    language = config['USER_LANGUAGE']

    # update the (previous) text
    if idx_current >= 0:
        doc_id = session_ids[idx_current]
        doc_labels = [sdg_id for sdg_id, n_clicks in enumerate(n_clicks_sdgs, start=1) if n_clicks % 2 == 1]
        database.update_paragraph(doc_id, doc_labels, email)

    ctx = callback_context
    # increase counter on first load automatically
    if ctx.triggered_id == 'next-button' or n_clicks_next == 0:
        idx_next = idx_current + 1
    elif ctx.triggered_id == 'back-button':
        idx_next = max(idx_current - 1, 0)  # prevent from going past before the first
    else:
        # probably never triggered
        idx_next = idx_current

    doc_id = session_ids[idx_next]
    if doc_id is None:
        doc = database.get_paragraph(language, email)
        selected_sgds = None
    else:
        doc = database.get_paragraph_by_id(doc_id)
        selected_sgds = utils.get_user_labels(doc, email)

    if idx_next == len(session_ids):
        return no_update, no_update, no_update, no_update, components.get_finish_layout(reason='session_done'), config
    elif doc is None:
        return no_update, no_update, no_update, no_update, components.get_finish_layout(reason='no_tasks'), config
    else:
        session_ids[idx_next] = doc['_id']

    sdg_buttons = components.get_sdg_buttons(selected_sgds)
    value = idx_current / len(session_ids) * 100
    config['IDX_CURRENT'] = idx_next
    config['SESSION_IDS'] = session_ids
    return value, f'{value:.0f}%', sdg_buttons, doc['text'], no_update, config


@callback(
    Output({'type': 'sdg-button', 'index': MATCH}, 'style'),
    Input({'type': 'sdg-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'sdg-button', 'index': MATCH}, 'id'),
    prevent_initial_call=True
)
def change_sdg_img(n_clicks, button_id):
    is_selected = n_clicks % 2 == 1
    sdg_id = button_id['index']
    style = styles.get_sdg_style(sdg_id=sdg_id, is_selected=is_selected)
    return style
