# dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# local packages
from src import entities, utils
from src.ui import styles


def insert_accordion_sdg(sdg: entities.SustainableDevelopmentGoal):
    list_targets = dmc.List([dmc.ListItem(target) for target in sdg.targets], spacing=10)
    item_control = dmc.AccordionControl(f'Goal {sdg.id}: {sdg.name}')
    item_panel = dmc.AccordionPanel(list_targets)
    item = dmc.AccordionItem(
        children=[item_control, item_panel],
        value=str(sdg.id),
    )
    return item


def insert_drawer_reference():
    sdgs = utils.read_sdg_metadata()
    items = [insert_accordion_sdg(sdg) for sdg in sdgs]
    accordion = dmc.Accordion(children=items,)
    text = dmc.Text('Click on an SDG below to see more details about it.')

    nav_link = dmc.NavLink(
        label='Want to learn even more about SDGs?',
        href='https://www.undp.org/sustainable-development-goals',
        target='_blank',
        icon=DashIconify(icon='bi:house-door-fill', height=16),
        active=True,
        variant='subtle',
        color=styles.PRIMARY_COLOUR,
        rightSection=DashIconify(icon='tabler-chevron-right'),
    )

    stack = dmc.Stack(
        children=[
            text,
            nav_link,
            dmc.ScrollArea(accordion, h=1000),  # this needs some adjustments
        ]
    )
    drawer = dmc.Drawer(
        title=dmc.Text('SDG Reference', weight=700),  # bold
        children=stack,
        id='drawer-reference',
        size='lg',
        padding='md',
        zIndex=10000,
    )
    return drawer
