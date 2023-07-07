# web app
import dash
import dash_mantine_components as dmc

# local packages
import src

dash.register_page(__name__, path='/login')


def layout():
    spans = {
        'xl': 9,
        'lg': 9,
        'md': 10,
        'sm': 11,
        'xs': 11,
    }

    columns = [
        *src.ui.header.insert_header(),
        dmc.Col(src.ui.accordions.insert_accordion_announcements(), **spans),
        dmc.Col(src.ui.accordions.insert_accordion_leaderboard(), **spans),
        dmc.Col(src.ui.layouts.insert_login_elements(), **spans, id='login-settings'),
        dmc.Col(src.ui.layouts.insert_session_elements(), **spans, id='session-settings', style={'display': 'none'}),
        dmc.Col(src.ui.footer.insert_footer(), span=12),
    ]

    page = dmc.Grid(
        id='content',
        children=columns,
        justify='center',
        gutter='sm',
    )
    return page
