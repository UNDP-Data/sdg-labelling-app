# web app
from dash import callback, no_update, callback_context, dcc, ALL, MATCH
from dash.dependencies import Input, Output, State

# local packages
import src


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
    config = src.entities.SessionConfig(**config)
    progress = (sum(task_id is not None for task_id in config.task_ids) - 1) / len(config.task_ids) * 100
    n_labels = src.database.get_stats_user(config)
    user_stats = src.ui.extras.insert_user_stats(n_labels)
    button_back_disabled = config.task_idx <= 0
    button_next_name = 'Next & Finish' if config.task_idx == (len(config.task_ids) - 1) is not None else 'Next'
    return progress, f'{progress:.0f}%', user_stats, button_back_disabled, button_next_name


@callback(
    Output('chip-container', 'children'),
    Output('chip-container', 'style'),
    Output('paragraph', 'children'),
    Output('paragraph', 'style'),
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
def navigate_texts(n_clicks_next, n_clicks_back, config, n_clicks_sdgs, comment):
    """Update the components of the main layout and the database with the current state of the labeling."""
    config = src.entities.SessionConfig(**config)
    ctx = callback_context
    # increase counter on first load automatically
    if ctx.triggered_id == 'next-button':
        doc_id = config.get_task_id()
        config.task_idx += 1
        annotation = src.entities.Annotation(
            created_by=config.user_id,
            labels=[sdg_id for sdg_id, n_clicks in enumerate(n_clicks_sdgs, start=1) if n_clicks % 2 == 1],
            comment=comment,
        )
        src.database.update_paragraph(doc_id, annotation)
    elif ctx.triggered_id == 'back-button':
        config.task_idx = max(config.task_idx - 1, 0)
    else:
        # probably never triggered
        pass

    # finish the session once the specified number of examples has been labelled
    if config.task_idx == len(config.task_ids):
        redirect = dcc.Location(id='redirect', pathname='/quit', refresh=True)
        return no_update, no_update, no_update, no_update, redirect, config.dict(), no_update

    doc_id = config.get_task_id()
    if doc_id is None:
        doc = src.database.get_paragraph(config)
        selected_sgds, comment = None, None

        # finish the session if there are no more unlabelled examples for a given user and language
        if doc is None:
            redirect = dcc.Location(id='redirect', pathname='/quit', refresh=True)
            return no_update, no_update, no_update, no_update, redirect, config.dict(), no_update
    else:
        doc = src.database.get_paragraph_by_id(doc_id)
        selected_sgds, comment = src.utils.get_user_label_and_comment(doc, config.user_id)

    sdg_buttons = src.ui.buttons.insert_buttons_sdg(selected_sgds, language=config.language)
    config.set_task_id(doc['_id'])
    # reverse text and icon order for Arabic
    style_icons = {'width': '100%'} | ({} if config.language != 'ar' else {'flex-direction': 'row-reverse'})
    style_text = {'direction': 'ltr' if config.language != 'ar' else 'rtl'}

    return sdg_buttons, style_icons, doc['text'], style_text, no_update, config.dict(), comment


@callback(
    Output({'type': 'sdg-button', 'index': MATCH}, 'style'),
    Input({'type': 'sdg-button', 'index': MATCH}, 'n_clicks'),
    State({'type': 'sdg-button', 'index': MATCH}, 'id'),
    State('session-config', 'data'),
    prevent_initial_call=True
)
def switch_sdg_icon(n_clicks, button_id, config):
    is_selected = n_clicks % 2 == 1
    sdg_id = button_id['index']
    style = src.ui.styles.get_sdg_style(sdg_id=sdg_id, is_selected=is_selected, language=config['language'])
    return style


@callback(
    Output('drawer-reference', 'opened'),
    Input('drawer-button', 'n_clicks'),
    prevent_initial_call=True,
)
def open_drawer_reference(n_clicks):
    is_open = n_clicks is not None
    return is_open


@callback(
    Output('modal-quit', 'opened', allow_duplicate=True),
    Input('quit-button', 'n_clicks'),
    prevent_initial_call=True
)
def open_modal_quit(n_clicks):
    is_open = n_clicks is not None
    return is_open


@callback(
    Output('notifications-container', 'children', allow_duplicate=True),
    Input('quit-modal-button', 'n_clicks'),
    prevent_initial_call=True

)
def quit_app(n_clicks):
    """Quit the app and change the layout to the start layout."""
    ctx = callback_context
    if ctx.triggered_id == 'quit-modal-button' and n_clicks is not None:
        return dcc.Location(id='redirect', pathname='/quit', refresh=True)
    else:
        return no_update
