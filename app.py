# Import packages
from dash import Dash, html, dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash._callback_context
import dash_mantine_components as dmc
from math import floor
from dotenv import load_dotenv
import os
from json import dumps
# import ast
import pymongo
# import dash_auth
import scripts.script as script
import scripts.components as components

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')


# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client['sdg_text_corpora']
collection = db['test']


# All the valid username/password pairs come from .env file for now
# User validation and control is yet to be implemented.

# VALID_USERNAME_PASSWORD_PAIRS = ast.literal_eval(
#    os.environ.get('VALID_USERNAME_PASSWORD_PAIRS'))


# Initialize the app
external_stylesheets = ['styles.css']
app = Dash(__name__,
           external_stylesheets=external_stylesheets,
           meta_tags=[{
               "name": "viewport",
               "content": 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5, user-scalable=yes'

           }],
           prevent_initial_callbacks='initial_duplicate',
           suppress_callback_exceptions=True
           )

# User validation and control is yet to be implemented.
"""auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
"""

# Initialize components


app.layout = dmc.MantineProvider(
    children=[
        dcc.Store(id='memory-output', storage_type='memory'),
        html.Div(
            id='app-wrapper',
            children=components.START_LAYOUT
        )
    ]
)

# Callbacks


@app.callback(
    [Output('app-wrapper', 'children', allow_duplicate=True)],
    [Input('start-over-button', 'n_clicks')]
)
def start_over_button(n_clicks):
    """This callback resets the app to its initial state when the start over button is clicked."""
    if n_clicks is not None:
        return [components.START_LAYOUT]
    else:
        return dash.no_update


@app.callback(
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
        return components.START_LAYOUT, False
    else:
        return dash.no_update, is_open


@app.callback(
    [Output('app-wrapper', 'children', allow_duplicate=True),
     Output('memory-output', 'data',  allow_duplicate=True)],
    Input('start-button', 'n_clicks'),
    [State('slider', 'value'),
    State('memory-output', 'data')],
    prevent_initial_call=True
)
def changeToMainLayout(n_clicks, input_value, data):
    """Change start layout to main layout."""
    if n_clicks is not None:
        doc = list(script.get_paragraphs(collection))[0]
        aux = {
            'N_CLICKS': 0,
            'MAX_CLICKS': input_value,
            'LABELS': [[] for i in range(input_value)],
            'CURRENT_DOC': doc,
            'DOC_IDS': [doc['_id']]
        }
        x = components.get_main_layout(doc['text'])
        return x, aux
    else:
        raise PreventUpdate


@app.callback(
    [Output('app-wrapper', 'children', allow_duplicate=True)],
    [Input('next-button', 'n_clicks')],
    State('memory-output', 'data'),
    prevent_initial_call=True
)
def changeToFinishLayout(n_clicks, data):
    """Change main layout to finish layout."""
    clk = data['N_CLICKS']
    max_clk = data['MAX_CLICKS']

    if n_clicks is not None and clk == max_clk:
        return components.FINISH_LAYOUT
    else:
        raise PreventUpdate


@app.callback(
    Output("modal", "opened", allow_duplicate=True),
    Input("quit-button", "n_clicks"),
    prevent_initial_call=True
)
def toggle_modal(n_clicks):
    """Toggle the modal."""
    return True if n_clicks is not None else False


@app.callback(
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
def update_components(n_clicks_next, n_clicks_back, chip_container_children: list[dmc.Tooltip], data):
    """Update the components of the main layout and the database with the current state of the labeling."""
    user_clicks = data['N_CLICKS']
    max_clicks = data['MAX_CLICKS']
    doc = data['CURRENT_DOC']
    labels = data['LABELS']
    doc_ids = data['DOC_IDS']

    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = ''
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # uncheck chips
    aux = []
    for tooltip in chip_container_children:
        chip = tooltip['props']['children'][0]['props']
        if chip['checked'] == True:
            aux.append(int(chip['value']))
            chip['checked'] = False

    if button_id == 'next-button' and n_clicks_next is not None:
        labels[user_clicks] = aux
        user_clicks += 1

        # update database with the current state of the labeling
        if aux != []:
            script.update_paragraph(collection, doc['_id'], aux)

        # get next paragraph
        if user_clicks < max_clicks:
            aux = labels[user_clicks]
            if doc_ids[-1] != doc['_id']:
                doc = script.get_paragraph_by_id(
                    collection, doc_ids[user_clicks])
            else:
                paragraphs = script.get_paragraphs(collection)
                i = 0
                while paragraphs[i]['_id'] in doc_ids:
                    i += 1
                doc = paragraphs[i]
                doc_ids.append(doc['_id'])

            # check chips if neccesary
            if labels[user_clicks] != []:
                for tooltip in chip_container_children:
                    chip = tooltip['props']['children'][0]['props']
                    if int(chip['value']) in aux:
                        chip['checked'] = True

    elif button_id == 'back-button' and n_clicks_back is not None and user_clicks > 0:
        labels[user_clicks] = aux
        user_clicks -= 1
        aux = labels[user_clicks]
        doc = script.get_paragraph_by_id(collection, doc_ids[user_clicks])

        # check chips
        for tooltip in chip_container_children:
            chip = tooltip['props']['children'][0]['props']
            if int(chip['value']) in aux:
                chip['checked'] = True

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
        'DOC_IDS': doc_ids
    }

    # get next paragraph
    if value < 100:
        return value, str(floor(value)) + '%', chip_container_children, doc['text'], dash.no_update, aux
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, components.FINISH_LAYOUT, aux


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
