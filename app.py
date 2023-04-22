# Import packages
from dash import Dash, html, dcc
import dash_mantine_components as dmc
from scripts.components import get_start_layout
import scripts.callbacks as callbacks


# Initialize the app
app = Dash(__name__,
           external_stylesheets=['styles.css'],
           meta_tags=[{
               "name": "viewport",
               "content": 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5, user-scalable=yes'

           }],
           prevent_initial_callbacks='initial_duplicate',
           suppress_callback_exceptions=True
           )


# Initialize components

app.layout = dmc.MantineProvider(
    children=[
        dcc.Store(id='memory-output', storage_type='memory'),
        html.Div(
            id='app-wrapper',
            children=get_start_layout()
        )
    ]
)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
