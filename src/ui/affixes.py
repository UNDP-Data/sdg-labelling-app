# standard library
import os

# dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# local packages
from src.ui import styles, buttons


def insert_affix_reference():
    affix = dmc.Affix(
        children=buttons.insert_button_reference(),
        position={'bottom': 25, 'left': 5},
    )
    return affix


def insert_affix_feedback():
    text = dmc.Text(
        'Feedback',
        color=styles.PRIMARY_COLOUR,
        variant='gradient'
    )
    icon = dmc.ActionIcon(
        DashIconify(
            icon='ic:outline-feedback',
            width=50,
            color=styles.PRIMARY_COLOUR,
        ),
        size='lg',
        mb=10,
    )

    anchor = dmc.Anchor(
        children=dmc.Group([text, icon]),
        href=os.environ['MAILTO'],
        underline=False,
    )

    affix = dmc.Affix(
        children=anchor,
        position={'bottom': 25, 'right': 5}
    )
    return affix
