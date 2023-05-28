# standard library
from typing import get_args

# dash
from dash import callback, callback_context, no_update, MATCH, ALL
from dash.dependencies import Input, Output, State

# local packages
from src import database, components, styles, entities, utils, communication


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
    Output('modal-faq', 'opened'),
    Input('faq-button', 'n_clicks'),
    prevent_initial_call=True
)
def open_faq(n_clicks):
    is_open = n_clicks is not None
    return is_open


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
def change_to_main_layout(n_clicks, input_value, language, email, access_code):
    """Change start layout to main layout."""
    user_id = utils.get_user_id(email)
    is_valid_email = utils.validate_email(email=email)
    is_valid_code = database.validate_user_code(user_id=user_id, access_code=access_code)

    if not is_valid_email:
        return no_update, no_update, 'Invalid email address', no_update
    elif not is_valid_code:
        return no_update, no_update, no_update, 'Invalid invitation code'
    else:
        config = entities.SessionConfig(
            task_idx=0,
            task_ids=[None] * input_value,
            user_id=user_id,
            language=language,
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
    Output('progress-bar', 'value'),
    Output('progress-bar', 'label'),
    Output('user-stats', 'children'),
    Output('back-button', 'disabled'),
    Output('next-button', 'children'),
    Input('session-config', 'data'),
    prevent_initial_call=True,
)
def update_controls(config):
    config = entities.SessionConfig(**config)
    progress = (sum(task_id is not None for task_id in config.task_ids) - 1) / len(config.task_ids) * 100
    n_labels = database.get_stats_user(config)
    user_stats = components.insert_user_stats(n_labels)
    button_back_disabled = config.task_idx <= 0
    button_next_name = 'Next & Finish' if config.task_idx == (len(config.task_ids) - 1) is not None else 'Next'
    return progress, f'{progress:.0f}%', user_stats, button_back_disabled, button_next_name


@callback(
    [Output({'type': 'ring', 'index': iso}, 'sections') for iso in get_args(entities.LANGUAGE_ISO)],
    Input('interval-component', 'n_intervals'),
)
def update_stats(_: int):
    stats = database.get_stats_by_language()
    output = [[{'value': stats.get(iso, 0), 'color': styles.PRIMARY_COLOUR}] for iso in get_args(entities.LANGUAGE_ISO)]
    return output


@callback(
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
    prevent_initial_call=True
)
def update_components(n_clicks_next, n_clicks_back, config, n_clicks_sdgs, comment):
    """Update the components of the main layout and the database with the current state of the labeling."""
    config = entities.SessionConfig(**config)
    ctx = callback_context
    # increase counter on first load automatically
    if ctx.triggered_id == 'next-button':
        doc_id = config.get_task_id()
        config.task_idx += 1
        annotation = entities.Annotation(
            created_by=config.user_id,
            labels=[sdg_id for sdg_id, n_clicks in enumerate(n_clicks_sdgs, start=1) if n_clicks % 2 == 1],
            comment=comment,
        )
        database.update_paragraph(doc_id, annotation)
    elif ctx.triggered_id == 'back-button':
        config.task_idx = max(config.task_idx - 1, 0)
    else:
        # probably never triggered
        pass

    # finish the session once the specified number of examples has been labelled
    if config.task_idx == len(config.task_ids):
        final_layout = components.get_finish_layout(reason='session_done')
        return no_update, no_update, final_layout, config.dict(), no_update

    doc_id = config.get_task_id()
    if doc_id is None:
        doc = database.get_paragraph(config)
        selected_sgds, comment = None, None

        # finish the session if there are no more unlabelled examples for a given user and language
        if doc is None:
            final_layout = components.get_finish_layout(reason='no_tasks')
            return no_update, no_update, final_layout, config.dict(), no_update
    else:
        doc = database.get_paragraph_by_id(doc_id)
        selected_sgds, comment = utils.get_user_label_and_comment(doc, config.user_id)

    sdg_buttons = components.get_sdg_buttons(selected_sgds, language=config.language)
    config.set_task_id(doc['_id'])
    return sdg_buttons, doc['text'], no_update, config.dict(), comment


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
    style = styles.get_sdg_style(sdg_id=sdg_id, is_selected=is_selected, language=config['language'])
    return style


@callback(
    Output('drawer-reference', 'opened'),
    Input('drawer-button', 'n_clicks'),
    prevent_initial_call=True,
)
def open_sdg_reference(n_clicks):
    return True


@callback(
    Output('email-button', 'disabled', allow_duplicate=True),
    Output('start-button', 'disabled', allow_duplicate=True),
    Output('notifications-container', 'children', allow_duplicate=True),
    Input('email-button', 'disabled'),
    State('email-input', 'value'),
    prevent_initial_call=True,
)
def send_access_code_with_notification(disabled, email):
    user_id = utils.get_user_id(email)
    access_code = communication.send_access_code(email=email)
    if access_code is None:
        notification = components.get_notification_failed(email=email)
        is_disabled = False
    else:
        database.upsert_user_code(user_id=user_id, access_code=access_code)
        notification = components.get_notification_sent(email=email)
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
    if not utils.validate_email(email=email):
        error_message = 'Invalid email address'
        return error_message, no_update, no_update
    notification = components.get_notification_sending(email=email)
    is_disabled = True
    error_message = None
    return error_message, is_disabled, is_disabled, notification
