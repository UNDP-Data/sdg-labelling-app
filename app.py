# dash
import dash
import dash_mantine_components as dmc
from dash import Dash, dcc, html

# utils
from dotenv import load_dotenv; load_dotenv()

# local packages
from src import callbacks

# app definition
dash_app = Dash(
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
    use_pages=True,
)
app = dash_app.server

# define layout
dash_app.layout = dmc.MantineProvider(
    dmc.NotificationsProvider(
        children=[
            dcc.Location(id='location'),
            dcc.Store(id='user-config', storage_type='session'),
            dcc.Store(id='session-config', storage_type='session'),
            dcc.Interval(
                id='interval-component',
                interval=1_000 * 10,  # in milliseconds
                n_intervals=0
            ),
            dash.page_container,
            html.Div(id='notifications-container'),
            html.Div(id='login-redirect'),
        ],
        autoClose=False,
        position='top-center',
    ),
    theme={
        "fontFamily": "'Proxima Nova', sans-serif",
        "headings":{
            "fontFamily": "SohneBreit, 'Proxima Nova', sans-serif",
            "sizes": {
                "h1":{"fontSize": "2.938rem"},
                "h2":{"fontSize": "2.5rem"},
                "h3":{"fontSize": "1.875rem"},
                "h4":{"fontSize": "1.563rem"},
                "h5":{"fontSize": "1.25rem"},
            },
            "fontWeight": "CSSProperties['fontWeight']",
            "lineHeight": "CSSProperties['lineHeight']",
        },
    },
)

# run the app
if __name__ == '__main__':
    dash_app.run_server(host='0.0.0.0', port=8050, debug=True)
