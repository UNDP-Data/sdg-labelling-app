# dash
from dash import callback, callback_context, no_update, MATCH, ALL
from dash.exceptions import PreventUpdate
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
        return components.get_finish_layout(), False
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
        doc = database.get_paragraph(language, email)
        config = {
            'N_CLICKS': 0,
            'MAX_CLICKS': input_value,
            'LABELS': [[] for _ in range(input_value)],
            'CURRENT_DOC': doc,
            'SESSION_IDS': [None] * input_value,
            'USER_LANGUAGE': language,
            'USER_EMAIL': email,
        }
        return components.get_main_layout(doc['text']), config, no_update
    else:
        return no_update, no_update, 'Invalid email address'


@callback(
    Output('content', 'children', allow_duplicate=True),
    Input('next-button', 'n_clicks'),
    State('session-config', 'data'),
    prevent_initial_call=True
)
def change_to_finish_layout(n_clicks, config):
    """Change main layout to finish layout."""
    if config['N_CLICKS'] == config['MAX_CLICKS']:
        return components.get_finish_layout()
    else:
        raise PreventUpdate
    

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
    user_clicks = config['N_CLICKS']
    max_clicks = config['MAX_CLICKS']
    doc = config['CURRENT_DOC']
    labels = config['LABELS']
    session_ids = config['SESSION_IDS']
    email = config['USER_EMAIL']
    language = config['USER_LANGUAGE']

    ctx = callback_context
    button_id = ctx.triggered_id

    # get labels from chips
    doc_labels = [sdg_id for sdg_id, n_clicks in enumerate(n_clicks_sdgs, start=1) if n_clicks % 2 == 1]
    labels[user_clicks] = doc_labels
    if button_id == 'next-button':
        session_ids[user_clicks] = doc['_id']
        database.update_paragraph(doc['_id'], doc_labels, email)
        user_clicks += 1

        if user_clicks == max_clicks:
            return no_update, no_update, no_update, no_update, components.get_finish_layout(), config
        elif session_ids[user_clicks] is not None:
            doc = database.get_paragraph_by_id(session_ids[user_clicks])
        else:
            doc = database.get_paragraph(language, email)

    elif button_id == 'back-button' and user_clicks > 0:
        user_clicks -= 1
        if user_clicks < 0:
            raise PreventUpdate
        doc = database.get_paragraph_by_id(session_ids[user_clicks])

    # check chips
    sdg_buttons = components.get_sdg_buttons(labels[user_clicks])
    value = user_clicks / max_clicks * 100
    config = {
        'N_CLICKS': user_clicks,
        'MAX_CLICKS': max_clicks,
        'LABELS': labels,
        'CURRENT_DOC': doc,
        'SESSION_IDS': session_ids,
        'USER_LANGUAGE': language,
        'USER_EMAIL': email
    }
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
