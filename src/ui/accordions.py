# dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# local packages
from .alerts import insert_alert_announcements
from .tables import insert_table_leaderboard
from . import styles


def insert_accordion_announcements():
    alerts = insert_alert_announcements()
    badge = dmc.Badge(
        children=len(alerts),
        color='red',
        variant='light',
        size='sm',
    )

    title = dmc.Group(
        children=['Announcements', badge],
        spacing='xs',
    )

    icon = DashIconify(
        icon='tabler:alert-triangle-filled',
        color='red',
        width=20,
    )

    stack = dmc.Stack(
        children=alerts,
        spacing='md',
    )

    accordion_item = dmc.AccordionItem(
        children=[
            dmc.AccordionControl(children=title, icon=icon),
            dmc.AccordionPanel(stack),
        ],
        value='announcements',
    )

    accordion = dmc.Accordion(
        children=accordion_item,
        variant='contained',
    )

    return accordion


def insert_accordion_leaderboard():
    badge = dmc.Badge(
        children='New',
        color=styles.PRIMARY_COLOUR,
        variant='light',
        size='sm',
    )

    title = dmc.Group(
        children=['Leaderboard', badge],
        spacing='xs',
    )

    icon = DashIconify(
        icon='tabler:list-numbers',
        color=styles.PRIMARY_COLOUR,
        width=20,
    )

    description = dmc.Text(
        children='If you want your name to appear on the leaderboard, log in to the application, open "My Profile",'
                 ' and turn on the switch next to "Display on Leaderboard".',
        size='sm',
    )

    stack = dmc.Stack(
        children=[
            description,
            insert_table_leaderboard(),
        ],
        spacing='md',
    )

    accordion_item = dmc.AccordionItem(
        children=[
            dmc.AccordionControl(children=title, icon=icon),
            dmc.AccordionPanel(stack),
        ],
        value='announcements',
    )

    accordion = dmc.Accordion(
        children=accordion_item,
        variant='contained',
    )

    return accordion
