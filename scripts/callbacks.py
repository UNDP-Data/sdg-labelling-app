# Import packages
from dash import callback, MATCH, ALL
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash._callback_context
from math import floor
from . import database
from . import components


@callback(
    [Output('app-wrapper', 'children', allow_duplicate=True)],
    [Input('start-over-button', 'n_clicks')],
    prevent_initial_call=True
)
def start_over_button(n_clicks):
    """This callback resets the app to its initial state when the start over button is clicked."""
    if n_clicks is not None:
        return [components.get_start_layout()]
    else:
        return dash.no_update
    
@callback(
    [Output('app-wrapper', 'children'),
     Output("modal", "opened", allow_duplicate=True)],
    Input('quit-modal-button', 'n_clicks'),
    State('modal', 'opened'),
    prevent_initial_call=True

)
def quit_app(n1, is_open):
    """Quit the app and change the layout to the start layout."""
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = ''
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'quit-modal-button' and n1 is not None:
        return components.get_start_layout(), False
    else:
        return dash.no_update, is_open
    
@callback(
    [Output('app-wrapper', 'children', allow_duplicate=True),
     Output('memory-output', 'data',  allow_duplicate=True)],
    Input('start-button', 'n_clicks'),
    [State('slider', 'value'),
    State('memory-output', 'data')],
    prevent_initial_call=True
)
def change_to_main_layout(n_clicks, input_value, data):
    """Change start layout to main layout."""
    if n_clicks is not None:
        doc, doc_ids, recent_ids = list(database.get_paragraph([], database.get_recent_ids()))
        aux = {
            'N_CLICKS': 0,
            'MAX_CLICKS': input_value,
            'LABELS': [[] for i in range(input_value)],
            'CURRENT_DOC': doc,
            'DOC_IDS': doc_ids,
            'RECENT_IDS': recent_ids
        }
        x = components.get_main_layout(doc['text'])
        return x, aux
    else:
        raise PreventUpdate
    


@callback(
    [Output('app-wrapper', 'children', allow_duplicate=True)],
    [Input('next-button', 'n_clicks')],
    State('memory-output', 'data'),
    prevent_initial_call=True
)
def change_to_finish_layout(n_clicks, data):
    """Change main layout to finish layout."""
    clk = data['N_CLICKS']
    max_clk = data['MAX_CLICKS']

    if n_clicks is not None and clk == max_clk:
        return components.get_finish_layout()
    else:
        raise PreventUpdate
    

@callback(
    Output("modal", "opened", allow_duplicate=True),
    Input("quit-button", "n_clicks"),
    prevent_initial_call=True
)
def toggle_modal(n_clicks):
    """Toggle the modal."""
    return True if n_clicks is not None else False

@callback(
    [Output('progress-bar', 'value'),
     Output('progress-bar', 'label'),
     Output('chip-container', 'children'),
     Output('paper', 'children'),
     Output('app-wrapper', 'children', allow_duplicate=True),
     Output('memory-output', 'data', allow_duplicate=True)],
    [Input('next-button', 'n_clicks'),
     Input('back-button', 'n_clicks')],
    State('chip-container', 'children'),
    State('memory-output', 'data'),
    prevent_initial_call=True
)
def update_components(n_clicks_next, n_clicks_back, chip_container_children, data):
    """Update the components of the main layout and the database with the current state of the labeling."""
    user_clicks = data['N_CLICKS']
    max_clicks = data['MAX_CLICKS']
    doc = data['CURRENT_DOC']
    labels = data['LABELS']
    doc_ids = data['DOC_IDS']
    recent_ids = data['RECENT_IDS']

    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = ''
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # get labels from chips
    aux = []
    for sdg in chip_container_children:
        if sdg['props']['children'][0]['props']['data']['clicked'] == True:
            aux.append(int(sdg['props']['children'][1]['props']['value']))
    
        

    if button_id == 'next-button' and n_clicks_next is not None:
        labels[user_clicks] = aux
        user_clicks += 1

        # update database with the current state of the labeling
        #if aux != []:
         #   database.update_paragraph(collection, doc['_id'], aux)

        # get next paragraph
        if user_clicks < max_clicks:
            aux = labels[user_clicks]
            if doc_ids[-1] != doc['_id']:
                doc = database.get_paragraph_by_id(doc_ids[user_clicks])
            else:
                doc, doc_ids, recent_ids = database.get_paragraph(doc_ids, recent_ids)
    
            # check chips if neccesary
            
            if labels[user_clicks] != []:
                chip_container_children = components.get_checked_chip_array(labels[user_clicks])
            

    elif button_id == 'back-button' and n_clicks_back is not None and user_clicks > 0:
        labels[user_clicks] = aux
        user_clicks -= 1
        aux = labels[user_clicks]
        doc = database.get_paragraph_by_id( doc_ids[user_clicks])

        # check chips
        if labels[user_clicks] != []:
                chip_container_children = components.get_checked_chip_array(labels[user_clicks])
            
    if user_clicks < max_clicks:
        if labels[user_clicks] == []:
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
        'RECENT_IDS': recent_ids
    }

    # get next paragraph
    if value < 100:
        return value, str(floor(value)) + '%', chip_container_children, doc['text'], dash.no_update, aux
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, components.get_finish_layout(), aux


@callback(
    [Output({'type': 'sdg-button', 'index': MATCH}, 'style'),
     Output({'type': 'sdg-store', 'index': MATCH}, 'data')],
    Input({'type': 'sdg-button', 'index': MATCH}, 'n_clicks'),
    [State({'type': 'sdg-button', 'index': MATCH}, 'id'),
     State({'type': 'sdg-store', 'index': MATCH}, 'data')],
    prevent_initial_call=True
)
def change_sdg_img(n_clicks, button_id, data):

    if  n_clicks is not None:
        index = int(button_id['index'])
        if data['clicked'] == False:
            return {
                'height': '11vh',
                'width': '11vh',
                'max-height': '11vh',
                'max-width': '11vh',
                'background-image': 'url("../assets/SDG_icons/SDG'+str(index)+'.png")',
                'background-size': 'cover',
                'transition': '0.3s',
                'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                'border-radius': '5px'
            }, {'clicked': True}
        else:
            return {
                    'height': '10vh',
                    'width': '10vh',
                    'max-height': '10vh',
                    'max-width': '10vh',
                    'background-image': 'url("../assets/SDG_icons/SDG'+str(index)+'.png")',
                    'background-size': 'cover',
                    'transition': '0.3s',
                    'border': '2px solid '+ components.SDG_COLORS[index-1],
                    'border-radius': '5px',
                }, {'clicked': False}
