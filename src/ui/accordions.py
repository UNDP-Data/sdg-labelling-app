# dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# local packages
from .alerts import insert_alert_announcements


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
