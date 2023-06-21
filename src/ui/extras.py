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
    for iso, name in sorted(utils.get_language_mapping().items(), key=lambda x: x[0]):
        ring = dmc.RingProgress(
            id={'type': 'ring', 'index': iso},
            label=dmc.Center(dmc.Text(iso.upper(), color=styles.PRIMARY_COLOUR)),
            size=65,
            thickness=5,
            roundCaps=False,
            sections=[{'value': 0, 'color': styles.PRIMARY_COLOUR}],
        )

        target = int(os.environ['PER_LANGUAGE_GOAL'])
        ring_with_tooltip = dmc.Tooltip(
            label=f'Progress in collecting {target:,} labels for {name}. Updates every few seconds.',
            style={'cursor': 'pointer'},
            children=ring,
            withArrow=True,
            openDelay=1_000,
        )
        rings.append(ring_with_tooltip)
    return rings


def insert_user_stats(n_labels: int):
    badge = dmc.Badge(f'you labelled {n_labels:,} texts', color='red', variant='light')
    return badge


def insert_user_count(count: int):
    badge = dmc.Badge(f'{count:,} people contributed', color='blue', variant='light')
    return badge


def insert_user_stack():
    stack = dmc.Stack(
        children=[
            dmc.Group(id='user-count', spacing='xs'),
            dmc.Group(id='user-stats', spacing='xs'),
        ]
    )
    return stack
