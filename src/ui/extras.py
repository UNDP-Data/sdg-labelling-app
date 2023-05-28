# standard library
import os

# dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# local packages
from src import utils
from src.ui import styles


def insert_rings_progress():
    rings = list()
    for iso, name in utils.get_language_mapping().items():
        ring = dmc.RingProgress(
            id={'type': 'ring', 'index': iso},
            label=dmc.Center(dmc.Text(iso.upper(), color=styles.PRIMARY_COLOUR)),
            size=80,
            thickness=10,
            roundCaps=False,
            sections=[{'value': 0, 'color': styles.PRIMARY_COLOUR}],
        )

        target = int(os.environ['PER_LANGUAGE_GOAL'])
        ring_with_tooltip = dmc.Tooltip(
            label=f'Progress in collecting {target:,} labelled examples for {name}. Updates every few seconds.',
            style={'cursor': 'pointer'},
            children=ring,
            withArrow=True,
            openDelay=1_000,
        )
        rings.append(ring_with_tooltip)
    return rings


def insert_user_stats(n_labels: int):
    text = dmc.Text('Your contribution', weight=100)
    badge = dmc.Badge(f'{n_labels} labels', color='red', variant='light')
    return [text, badge]


def insert_anchor_github():
    icon = DashIconify(
        icon='mdi:github',
        width=40,
        color='black',
    )
    anchor = dmc.Anchor(
        children=icon,
        href='https://github.com/UNDP-Data/sdg-labelling-app/issues',
        target='_blank',
    )
    return anchor
