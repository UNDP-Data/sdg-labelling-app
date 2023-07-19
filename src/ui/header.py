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
        size='lg',
        style={'overflow-wrap': 'break-word'},
    )

    title_stack = dmc.Stack(
        children=[title, subtitle],
        spacing='sm',
    )

    divider = dmc.Divider(
        color=styles.PRIMARY_COLOUR,
        variant='solid',
        className='header-divider'
    )

    progress_group = dmc.Group(
        children=extras.insert_rings_progress(),
        spacing='xs',
        style={'display': 'right'},
    )

    extra_group = dmc.Group(
        children=[
            extras.insert_user_stack(),
            buttons.insert_button_faq(),
            modals.insert_modal_faq(),
            modals.insert_modal_profile(),
            modals.insert_modal_statistics(),
            modals.insert_modal_quit(),
            insert_menu(),
        ],
        spacing='xs',
        style={'float': 'right'},
    )

    columns = [
        dmc.Col(title_stack, xl=5, lg=5, md=12, sm=12, xs=12),
        dmc.Col(progress_group, xl=4, lg=5, md=7, sm=7, xs=12),
        dmc.Col(extra_group, xl=3, lg=2, md=5, sm=5, xs=12),
        dmc.Col(divider, span=12),
    ]
    return columns
