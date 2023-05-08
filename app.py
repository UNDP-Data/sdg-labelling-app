# dash
import dash_mantine_components as dmc
from dash import Dash, html, dcc

# utils
from dotenv import load_dotenv; load_dotenv()

# local packages
from src import components, callbacks

# app definition
app = Dash(
    __name__,
    external_stylesheets=['styles.css'],
    meta_tags=[{
       'name': 'viewport',
       'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5, user-scalable=yes'

    }],
    prevent_initial_callbacks='initial_duplicate',
    suppress_callback_exceptions=True,
    title='SDG App',
    update_title='Loading...',
)

# define layout
app.layout = dmc.MantineProvider(
    children=[
        dcc.Store(id='session-config', storage_type='memory'),
        components.get_header(),
        dmc.Container(
            id='content',
            children=components.get_start_layout(),
            fluid=True,
        ),
        components.get_affix(),
    ]
)

# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
