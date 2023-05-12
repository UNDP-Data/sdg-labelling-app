# dash
from dash import callback, callback_context, no_update, MATCH, ALL
from dash.dependencies import Input, Output, State

# local packages
from src import database, components, styles, entities, utils


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
    Output('code-input', 'error'),
    Input('start-button', 'n_clicks'),
    State('slider', 'value'),
    State('language-input', 'value'),
    State('email-input', 'value'),
    State('code-input', 'value'),
    prevent_initial_call=True
)
def change_to_main_layout(n_clicks, input_value, language, email, code):
    """Change start layout to main layout."""
    if not utils.validate_email(email=email):
        return no_update, no_update, 'Invalid email address', no_update
    elif not utils.validate_code(code=code):
        return no_update, no_update, no_update, 'Invalid invitation code'
    else:
        config = entities.Config(
            task_idx=0,
            task_ids=[None] * input_value,
            session_language=language,
            session_email=email,
        )
        return components.get_main_layout(), config.dict(), no_update, no_update


@callback(
    Output('modal', 'opened', allow_duplicate=True),
    Input('quit-button', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_modal(n_clicks):
    """Toggle the modal."""
    return n_clicks is not None


@callback(
    Output('back-button', 'disabled'),
    Input('session-config', 'data'),
)
def disable_button_back(config):
    is_disabled = config['task_idx'] <= 0
    return is_disabled


@callback(
    Output('progress-bar', 'value'),
    Output('progress-bar', 'label'),
    Output('chip-container', 'children'),
    Output('paragraph', 'children'),
    Output('content', 'children', allow_duplicate=True),
    Output('session-config', 'data', allow_duplicate=True),
    Output('comment', 'value'),
    Input('next-button', 'n_clicks'),
    Input('back-button', 'n_clicks'),
    State('session-config', 'data'),
    State({'type': 'sdg-button', 'index': ALL}, 'n_clicks'),
    State('comment', 'value'),
    State('progress-bar', 'value'),
    prevent_initial_call=True
)
def update_components(n_clicks_next, n_clicks_back, config, n_clicks_sdgs, comment, progress):
    """Update the components of the main layout and the database with the current state of the labeling."""
    config = entities.Config(**config)
    ctx = callback_context
    # increase counter on first load automatically
    if ctx.triggered_id == 'next-button':
        doc_id = config.get_task_id()
        config.task_idx += 1
        annotation = entities.Annotation(
            email=config.session_email,
            labels=[sdg_id for sdg_id, n_clicks in enumerate(n_clicks_sdgs, start=1) if n_clicks % 2 == 1],
            comment=comment,
        )
        database.update_paragraph(doc_id, annotation)
        progress = config.task_idx / len(config.task_ids) * 100
    elif ctx.triggered_id == 'back-button':
        config.task_idx = max(config.task_idx - 1, 0)
    else:
        # probably never triggered
        pass

    # finish the session once the specified number of examples has been labelled
    if config.task_idx == len(config.task_ids):
        final_layout = components.get_finish_layout(reason='session_done')
        return no_update, no_update, no_update, no_update, final_layout, config.dict(), no_update

    doc_id = config.get_task_id()
    if doc_id is None:
        doc = database.get_paragraph(config)
        selected_sgds, comment = None, None

        # finish the session if there are no more unlabelled examples for a given user and language
        if doc is None:
            final_layout = components.get_finish_layout(reason='no_tasks')
            return no_update, no_update, no_update, no_update, final_layout, config.dict(), no_update
    else:
        doc = database.get_paragraph_by_id(doc_id)
        selected_sgds, comment = utils.get_user_label_and_comment(doc, config.session_email)

    sdg_buttons = components.get_sdg_buttons(selected_sgds, language=config.session_language)
    config.set_task_id(doc['_id'])
    return progress, f'{progress:.0f}%', sdg_buttons, doc['text'], no_update, config.dict(), comment


@callback(
    Output({'type': 'sdg-button', 'index': MATCH}, 'style'),
    Input({'type': 'sdg-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'sdg-button', 'index': MATCH}, 'id'),
    State('session-config', 'data'),
    prevent_initial_call=True
)
def change_sdg_img(n_clicks, button_id, config):
    is_selected = n_clicks % 2 == 1
    sdg_id = button_id['index']
    style = styles.get_sdg_style(sdg_id=sdg_id, is_selected=is_selected, language=config['session_language'])
    return style


@callback(
    Output('drawer-reference', 'opened'),
    Input('drawer-button', 'n_clicks'),
    prevent_initial_call=True,
)
def open_sdg_reference(n_clicks):
    return True
