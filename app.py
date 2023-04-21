# Import packages
from dash import Dash, html
from dash.dependencies import Input, Output, State
import dash._callback_context
import dash_mantine_components as dmc
from math import floor
from dotenv import load_dotenv
import os
#import ast
import pymongo
#import dash_auth
import scripts.script as script
import scripts.components as components

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')


# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client['sdg_text_corpora']
collection = db['test']


# Initialize constants
MAX_CLICKS = 30
N_CLICKS = 0

# list of doc ids for backwards navigation
DOC_IDS = []

# list of labels for backwards navigation
LABELS = []


# All the valid username/password pairs come from .env file for now
# User validation and control is yet to be implemented.

#VALID_USERNAME_PASSWORD_PAIRS = ast.literal_eval(
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
    global CURRENT_DOC

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
    [Output('app-wrapper', 'children', allow_duplicate=True)],
    [Input('start-button', 'n_clicks'),
     Input('slider', 'value')]
)
def changeToMainLayout(n_clicks, input_value):
    """Change start layout to main layout."""
    global MAX_CLICKS
    global N_CLICKS
    global LABELS
    global DOC_IDS
    global CURRENT_DOC

    if n_clicks is not None:
        N_CLICKS = 0
        MAX_CLICKS = input_value
        LABELS = [[] for i in range(MAX_CLICKS)]
        CURRENT_DOC = list(script.get_paragraphs(collection))[0]
        DOC_IDS = [CURRENT_DOC['_id']]
        return [components.get_main_layout(CURRENT_DOC['text'])]
    else:
        return dash.no_update


@app.callback(
    [Output('app-wrapper', 'children', allow_duplicate=True)],
    [Input('next-button', 'n_clicks')]
)
def changeToFinishLayout(n_clicks):
    """Change main layout to finish layout."""
    global N_CLICKS
    if n_clicks is not None and N_CLICKS == MAX_CLICKS:
        return components.FINISH_LAYOUT
    else:
        return dash.no_update


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
     Output('app-wrapper', 'children', allow_duplicate=True)],
    [Input('next-button', 'n_clicks'),
     Input('back-button', 'n_clicks')],
     State('chip-container', 'children'),
     prevent_initial_call=True
)
def update_components(n_clicks_next, n_clicks_back, chip_container_children: list[dmc.Tooltip]):
    """Update the components of the main layout and the database with the current state of the labeling."""
    global N_CLICKS
    global CURRENT_DOC

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
        LABELS[N_CLICKS] = aux
        N_CLICKS += 1
            

        # update database with the current state of the labeling
        if aux != []:
            script.update_paragraph(collection, CURRENT_DOC['_id'], aux)

        # get next paragraph
        if N_CLICKS < MAX_CLICKS:
            aux = LABELS[N_CLICKS]
            if DOC_IDS[-1] != CURRENT_DOC['_id']:
                CURRENT_DOC = script.get_paragraph_by_id(
                    collection, DOC_IDS[N_CLICKS])
            else:
                paragraphs = script.get_paragraphs(collection)
                i = 0
                while paragraphs[i]['_id'] in DOC_IDS:
                    i += 1
                CURRENT_DOC = paragraphs[i]
                DOC_IDS.append(CURRENT_DOC['_id'])

            # check chips if neccesary
            if LABELS[N_CLICKS] != []:
                for tooltip in chip_container_children:
                    chip = tooltip['props']['children'][0]['props']
                    if int(chip['value']) in aux:
                        chip['checked'] = True
        

    elif button_id == 'back-button' and n_clicks_back is not None and N_CLICKS > 0:
        LABELS[N_CLICKS] = aux
        N_CLICKS -= 1
        aux = LABELS[N_CLICKS]
        CURRENT_DOC = script.get_paragraph_by_id(collection, DOC_IDS[N_CLICKS])

        # check chips
        for tooltip in chip_container_children:
            chip = tooltip['props']['children'][0]['props']
            if int(chip['value']) in aux:
                chip['checked'] = True

    if N_CLICKS < 0:
        N_CLICKS = 0
    elif N_CLICKS > MAX_CLICKS:
        N_CLICKS = MAX_CLICKS

    value = N_CLICKS / MAX_CLICKS * 100

    # get next paragraph
    if value < 100:
        return value, str(floor(value)) + '%', chip_container_children, CURRENT_DOC['text'], dash.no_update
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, components.FINISH_LAYOUT


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
