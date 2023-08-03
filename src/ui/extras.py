# standard library
import os

# dash
import dash_mantine_components as dmc

# local packages
from src import utils


def insert_rings_progress():
    rings = list()
    for iso, name in sorted(utils.get_language_mapping().items(), key=lambda x: x[0]):
        ring = dmc.RingProgress(
            id={'type': 'ring', 'index': iso},
            label=dmc.Center(dmc.Text(iso.upper(), color='black')),
            size=65,
            thickness=5,
            roundCaps=False,
            rootColor='#D4D6D8',
            sections=[{'value': 0, 'color': "#EE402D"}],
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
    text = dmc.Text(f'You have labelled {n_labels:,} texts so far. More statistics are coming soon.')
    return text


def insert_user_count(count: int):
    text = dmc.Title(f'{count:,}', order=3)
    return text


def insert_stats_users():
    people_contributed = dmc.Text('people contributed')
    stats_users = dmc.Stack(
      children=[
          dmc.Group(id='user-count'),
          people_contributed,
      ],
      className='stat-card small'
    )
    return stats_users


def insert_progress_group():
    progress_group = dmc.Group(
      children=insert_rings_progress(),
      className='stat-card small'
    )
    return progress_group


def insert_stats_bar():
    group = dmc.Group(
      children=[
          insert_progress_group(),
          insert_stats_users(),
      ],
      className='stat-card-container',
    )
    return group
