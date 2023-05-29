# standard library
from typing import Literal

# dash
import dash_mantine_components as dmc

# local packages
from src.ui import styles, alets, buttons, inputs, modals, affixes, drawer


def get_start_layout():
    title = dmc.Title(
        'LET\'S GET STARTED',
        order=2,
        color=styles.PRIMARY_COLOUR,
        variant='gradient'
    )

    text = dmc.Text(
        'Select the number of texts you want to label',
        style={'text-align': 'center'},
        color=styles.PRIMARY_COLOUR,
    )

    group_passcode = dmc.Group(
        children=[inputs.insert_input_passcode(), buttons.insert_button_send()],
        position='center',
        grow=True,
        style={'width': '40%'},
    )

    stack = dmc.Stack(
        children=[
            *alets.insert_release_alerts(),
            title,
            text,
            inputs.insert_slider_texts(),
            inputs.insert_select_language(),
            inputs.insert_input_email(),
            group_passcode,
            buttons.insert_button_start(),
        ],
        align='center',
        spacing='xl',
        pt='3%',
        pb=25,
    )
    return stack


def get_main_layout():
    title = dmc.Title(
        'SELECT ONE OR MORE SDGs RELEVANT FOR THIS PARAGRAPH',
        order=2,
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
    )

    scroll = dmc.ScrollArea(
        children=dmc.Text('', id='paragraph'),
        h=200,  # may need to be better adjusted
    )

    paper = dmc.Paper(
        children=scroll,
        p='xl',
        shadow='lg',
        radius='md',
        withBorder=True,
        style={'font-size': 'large', 'min-height': '20vh'}
    )

    loading_paper = dmc.LoadingOverlay(
        children=paper,
        style={'width': '90%'},
    )

    labels = dmc.Container(
        id='chip-container',
        className='chip-container',
    )

    progress_bar = dmc.Progress(
        id='progress-bar',
        value=0,
        label='0%',
        color=styles.PRIMARY_COLOUR,
        radius='sm',
        size='xl',
        style={'width': '90%', 'margin': 'auto'}
    )

    stack = dmc.Stack(
        children=[
            title,
            progress_bar,
            loading_paper,
            labels,
            inputs.insert_select_comment(),
            buttons.insert_buttons_navigation(),
            modals.insert_modal_quit(),
            drawer.insert_drawer_reference(),
            affixes.insert_affix_reference(),
        ],
        align='center',
        spacing='xl',
        pt='3%',
        pb=25,
    )

    return stack


def get_finish_layout(reason: Literal['session_done', 'session_quit', 'no_tasks']):
    anchor_restart = dmc.Anchor(
        children=buttons.insert_button_restart(),
        href='/',
        refresh=True,
    )

    stack = dmc.Stack(
        children=[
            alets.insert_alert_finish(reason=reason),
            anchor_restart,
        ],
        align='center',
        spacing='xl',
        pt='3%',
        pb=25,
    )
    return stack
