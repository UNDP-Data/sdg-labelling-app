# web app
import dash
import dash_mantine_components as dmc

# local packages
import src

dash.register_page(__name__, path='/quit')


def layout():
    stack = dmc.Stack(
        children=[
            src.ui.alerts.insert_alert_finish(reason='session_done'),
            src.ui.buttons.insert_button_restart(),
        ],
        align='center',
        spacing='xl',
        pt='3%',
        pb=25,
    )

    spans = {
        'xl': 8,
        'lg': 10,
        'md': 12,
        'sm': 12,
        'xs': 12,
    }

    columns = [
        *src.ui.header.insert_header(),
        dmc.Col(stack, **spans),
        dmc.Col(src.ui.footer.insert_footer(), span=12),
    ]

    page = dmc.Grid(
        id='content',
        children=columns,
        justify='center',
        gutter='sm',
    )
    return page
