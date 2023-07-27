# standard library
import os

# dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# local packages
from src.ui import styles, buttons, modals, extras


def insert_menu():
    menu = dmc.Menu(
        [
            dmc.MenuTarget(dmc.Burger()),
            dmc.MenuDropdown(
                children=[
                    dmc.MenuLabel(
                        id={'type': 'menu-user', 'index': 'label'},
                        children='User',
                    ),
                    dmc.MenuItem(
                        id={'type': 'menu-user', 'index': 'profile'},
                        children=dmc.Group(['My Profile', dmc.Badge('New')], spacing='xs'),
                        icon=DashIconify(icon='tabler-user-circle'),
                        n_clicks=0,
                    ),
                    dmc.MenuItem(
                        id={'type': 'menu-user', 'index': 'statistics'},
                        children=dmc.Group(['My Statistics', dmc.Badge('New')], spacing='xs'),
                        icon=DashIconify(icon='tabler-report-analytics'),
                        n_clicks=0,
                    ),
                    dmc.MenuLabel('Community'),
                    dmc.MenuItem(
                        id={'type': 'menu-community', 'index': 'announcements'},
                        children=dmc.Group(['Announcements', dmc.Badge('New')], spacing='xs'),
                        icon=DashIconify(icon='tabler:alert-triangle-filled'),
                        n_clicks=0,
                    ),
                    dmc.MenuItem(
                        id={'type': 'menu-community', 'index': 'leaderboard'},
                        children=dmc.Group(['Leaderboard', dmc.Badge('New')], spacing='xs'),
                        icon=DashIconify(icon='tabler:list-numbers'),
                        n_clicks=0,
                    ),
                    dmc.MenuLabel('Feedback'),
                    dmc.MenuItem(
                        children='GitHub',
                        href='https://github.com/UNDP-Data/sdg-labelling-app/issues',
                        target='_blank',
                        icon=DashIconify(icon='radix-icons:external-link'),
                    ),
                    dmc.MenuItem(
                        children='Get in Touch',
                        href=os.environ['MAILTO'],
                        icon=DashIconify(icon='tabler-mail'),
                    )
                ]
            ),
        ],
    )
    return menu


def insert_header():
    title = dmc.Title(
        'SDG Labelling Application',
        order=1,
    )

    subtitle = dmc.Text(
        'Make Your Contribution Towards a Safer And More Inclusive Use of Artificial Intelligence for'
        ' International Development',
        style={'overflowWrap': 'break-word'},
        size='xl',
    )

    title_stack = dmc.Stack(
        children=[title, subtitle],
        spacing='xs',
        className='header-left',
    )

    divider = dmc.Divider(
        color=styles.PRIMARY_COLOUR,
        variant='solid',
        className='header-divider'
    )

    right_stack = dmc.Stack(
        children=[
            modals.insert_modal_announcements(),
            modals.insert_modal_leaderboard(),
            modals.insert_modal_faq(),
            modals.insert_modal_profile(),
            modals.insert_modal_statistics(),
            modals.insert_modal_quit(),
            insert_menu(),
            buttons.insert_button_faq(),
            extras.insert_user_stack(),
        ],
        spacing='xs',
        style={'float': 'right'},
        align='end',
        className='header-right',
    )

    columns = [
        dmc.Col(title_stack, xl=11, lg=11, md=11, sm=12, xs=12),
        dmc.Col(right_stack, xl=1, lg=1, md=1, sm=12, xs=12),
        dmc.Col(divider, span=12),
    ]
    return columns
