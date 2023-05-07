# standard library
from math import floor

# dash
from dash import callback, callback_context, no_update, MATCH
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

# local packages
from src import database, components, utils


@callback(
    Output('app-wrapper', 'children', allow_duplicate=True),
    Input('start-over-button', 'n_clicks'),
    prevent_initial_call=True
)
def start_over_button(n_clicks):
    """This callback resets the app to its initial state when the start over button is clicked."""
    if n_clicks is not None:
        return [components.get_start_layout()]
    else:
        return no_update


@callback(
    Output('app-wrapper', 'children'),
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
    Output('app-wrapper', 'children', allow_duplicate=True),
    Output('memory-output', 'data',  allow_duplicate=True),
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
        doc, doc_ids, recent_ids = list(database.get_paragraph([], database.get_recent_ids(), language, email))
        aux = {
            'N_CLICKS': 0,
            'MAX_CLICKS': input_value,
            'LABELS': [[] for i in range(input_value)],
            'CURRENT_DOC': doc,
            'DOC_IDS': doc_ids,
            'RECENT_IDS': recent_ids,
            'USER_LANGUAGE': language,
            'USER_EMAIL': email,
        }
        return components.get_main_layout(doc['text']), aux, no_update
    else:
        return no_update, no_update, 'Invalid email address'


@callback(
    Output('app-wrapper', 'children', allow_duplicate=True),
    Input('next-button', 'n_clicks'),
    State('memory-output', 'data'),
    prevent_initial_call=True
)
def change_to_finish_layout(n_clicks, data):
    """Change main layout to finish layout."""
    if data['N_CLICKS'] == data['MAX_CLICKS']:
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
    Output('app-wrapper', 'children', allow_duplicate=True),
    Output('memory-output', 'data', allow_duplicate=True),
    Input('next-button', 'n_clicks'),
    Input('back-button', 'n_clicks'),
    {
        'data': State('memory-output', 'data'),
        'sdgs': [State({'type': 'sdg-button', 'index': i}, 'n_clicks') for i in range(1, 18)]
    },
    prevent_initial_call=True
)
def update_components(n_clicks_next, n_clicks_back, states):
    """Update the components of the main layout and the database with the current state of the labeling."""
    data = states['data']
    user_clicks = data['N_CLICKS']
    max_clicks = data['MAX_CLICKS']
    doc = data['CURRENT_DOC']
    labels = data['LABELS']
    doc_ids = data['DOC_IDS']
    recent_ids = data['RECENT_IDS']
    email = data['USER_EMAIL']
    language = data['USER_LANGUAGE']

    ctx = callback_context
    button_id = ctx.triggered_id

    # get labels from chips
    aux = [sdg_id for sdg_id, n_clicks in enumerate(states['sdgs'], start=1) if n_clicks % 2 == 1]
    if button_id == 'next-button' and n_clicks_next is not None:
        labels[user_clicks] = aux
        user_clicks += 1

        # update database with the current state of the labeling
        if aux:
            database.update_paragraph(doc['_id'], aux, email)

        # get next paragraph
        if user_clicks < max_clicks:
            aux = labels[user_clicks]
            if doc_ids[-1] != doc['_id']:
                doc = database.get_paragraph_by_id(doc_ids[user_clicks])
            else:
                doc, doc_ids, recent_ids = database.get_paragraph(doc_ids, recent_ids, language, email)
    
            # check chips if neccesary
            
            if labels[user_clicks]:
                chip_container_children = components.get_checked_chip_array(labels[user_clicks])

    elif button_id == 'back-button' and n_clicks_back is not None and user_clicks > 0:
        labels[user_clicks] = aux
        user_clicks -= 1
        aux = labels[user_clicks]
        doc = database.get_paragraph_by_id(doc_ids[user_clicks])

        # check chips
        if labels[user_clicks]:
            chip_container_children = components.get_checked_chip_array(labels[user_clicks])
            
    if user_clicks < max_clicks:
        if not labels[user_clicks]:
            chip_container_children = components.get_blank_chip_array()

    if user_clicks < 0:
        user_clicks = 0
    elif user_clicks > max_clicks:
        user_clicks = max_clicks

    value = user_clicks / max_clicks * 100

    aux = {
        'N_CLICKS': user_clicks,
        'MAX_CLICKS': max_clicks,
        'LABELS': labels,
        'CURRENT_DOC': doc,
        'DOC_IDS': doc_ids,
        'RECENT_IDS': recent_ids,
        'USER_LANGUAGE': language,
        'USER_EMAIL': email
    }

    # get next paragraph
    if value < 100:
        return value, str(floor(value)) + '%', chip_container_children, doc['text'], no_update, aux
    else:
        return no_update, no_update, no_update, no_update, components.get_finish_layout(), aux


@callback(
    Output({'type': 'sdg-button', 'index': MATCH}, 'style'),
    Input({'type': 'sdg-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'sdg-button', 'index': MATCH}, 'id'),
    prevent_initial_call=True
)
def change_sdg_img(n_clicks, button_id):
    is_selected = n_clicks % 2 == 1
    sdg_id = button_id['index']
    style_selected = {
        'height': '11vh',
        'width': '11vh',
        'max-height': '11vh',
        'max-width': '11vh',
        'background-image': f'url("../assets/SDG_icons/color/en/sdg_{sdg_id}.png")',
        'background-size': 'cover',
        'border': '2px solid transparent',
        'transition': '0.3s',
        'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
        'border-radius': '5px',
        'cursor': 'pointer'
    }
    style_unselected = {
        'height': '10vh',
        'width': '10vh',
        'max-height': '10vh',
        'max-width': '10vh',
        'background-image': f'url("../assets/SDG_icons/black/en/sdg_{sdg_id}.png")',
        'background-size': 'cover',
        'transition': '0.3s',
        'border': '2px solid transparent',
        'border-radius': '5px',
        'cursor': 'pointer'
    }

    if is_selected:
        return style_selected
    return style_unselected
