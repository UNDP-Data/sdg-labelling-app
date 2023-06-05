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
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
    )

    subtitle = dmc.Text(
        'Make Your Contribution Towards a Safer And More Inclusive Use of Artificial Intelligence for'
        ' International Development',
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
        size='sm',
        style={'overflow-wrap': 'break-word'},
    )

    title_stack = dmc.Stack(
        children=[title, subtitle],
        spacing='sm',
    )

    divider = dmc.Divider(
        color=styles.PRIMARY_COLOUR,
        variant='solid',
    )

    spans_1 = {
        'xl': 4,
        'lg': 4,
        'md': 12,
        'sm': 12,
        'xs': 12,
    }

    spans_2 = {
        'xl': 2,
        'lg': 2,
        'md': 6,
        'sm': 6,
        'xs': 6,
    }

    columns = [
        dmc.Col(title_stack, **spans_1),
        dmc.Col(dmc.Group(extras.insert_rings_progress(), spacing='xs'), **spans_1),
        dmc.Col(extras.insert_user_stack(), **spans_2),
        dmc.Col(dmc.Group([buttons.insert_button_faq(), modals.insert_modal_faq(), insert_menu()],
                          spacing='xs'), **spans_2),
        dmc.Col(divider, span=12),
    ]
    return columns
