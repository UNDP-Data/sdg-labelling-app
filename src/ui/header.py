# standard library
import os

# dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# local packages
from src.ui import styles, buttons, modals, extras


def insert_menu():
    icon_size = 20
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
                        children='My Profile',
                        icon=DashIconify(icon='tabler-user-circle', width=icon_size),
                        n_clicks=0,
                    ),
                    dmc.MenuItem(
                        id={'type': 'menu-user', 'index': 'statistics'},
                        children='My Statistics',
                        icon=DashIconify(icon='tabler-report-analytics', width=icon_size),
                        n_clicks=0,
                    ),
                    dmc.MenuItem(
                        id={'type': 'menu-user', 'index': 'logout'},
                        children='Logout',
                        icon=DashIconify(icon='tabler:logout-2', width=icon_size),
                        n_clicks=0,
                    ),
                    dmc.MenuLabel('Community'),
                    dmc.MenuItem(
                        id={'type': 'menu-community', 'index': 'announcements'},
                        children='Announcements',
                        icon=DashIconify(icon='tabler:news', width=icon_size),
                        n_clicks=0,
                    ),
                    dmc.MenuItem(
                        id={'type': 'menu-community', 'index': 'leaderboard'},
                        children='Leaderboard',
                        icon=DashIconify(icon='tabler:list-numbers', width=icon_size),
                        n_clicks=0,
                    ),
                    dmc.MenuItem(
                        id={'type': 'menu-community', 'index': 'faq'},
                        children=dmc.Group(['FAQ', dmc.Badge('New')], spacing='xs'),
                        icon=DashIconify(icon='tabler:info-square-rounded', width=icon_size),
                        n_clicks=0,
                    ),
                    dmc.MenuLabel('Feedback'),
                    dmc.MenuItem(
                        children='GitHub',
                        href='https://github.com/UNDP-Data/sdg-labelling-app/issues',
                        target='_blank',
                        icon=DashIconify(icon='tabler:brand-github', width=icon_size),
                    ),
                    dmc.MenuItem(
                        children='Get in Touch',
                        href=os.environ['MAILTO'],
                        icon=DashIconify(icon='tabler-mail', width=icon_size),
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
