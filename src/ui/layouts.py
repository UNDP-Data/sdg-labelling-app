# standard library
from typing import Literal

# dash
import dash_mantine_components as dmc

# local packages
from src.ui import styles, alerts, buttons, inputs, modals, drawer, header, footer, affixes, accordions


def insert_login_elements():
    title = dmc.Title(
        'LOG IN',
        order=2,
        color=styles.PRIMARY_COLOUR,
        variant='gradient'
    )

    text = dmc.Text(
        'Enter Your Credentials to Proceed',
        style={'text-align': 'center'},
        color=styles.PRIMARY_COLOUR,
    )

    title_stack = dmc.Stack(
        children=[title, text],
        align='center',
    )

    login_stack = dmc.Stack(
        children=[
            title_stack,
            inputs.insert_input_email(),
            inputs.insert_input_passcode(),
            buttons.insert_button_send(),
            buttons.insert_button_login(),
        ],
        spacing='lg',
    )
    return login_stack


def insert_session_elements():
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

    title_stack = dmc.Stack(
        children=[title, text],
        align='center',
    )

    session_stack = dmc.Stack(
        children=[
            title_stack,
            inputs.insert_slider_texts(),
            inputs.insert_select_language(),
            buttons.insert_button_start(),
        ],
        spacing='lg',
    )
    return session_stack


def get_start_layout():
    spans = {
        'xl': 9,
        'lg': 9,
        'md': 10,
        'sm': 11,
        'xs': 11,
    }

    columns = [
        *header.insert_header(),
        dmc.Col(accordions.insert_accordion_announcements(), **spans),
        dmc.Col(accordions.insert_accordion_leaderboard(), **spans),
        dmc.Col(insert_login_elements(), **spans, id='login-settings'),
        dmc.Col(insert_session_elements(), **spans, id='session-settings', style={'display': 'none'}),
        dmc.Col(footer.insert_footer(), span=12),
    ]
    return columns


def get_main_layout():
    title = dmc.Title(
        'SELECT SDGs RELEVANT FOR THIS PARAGRAPH IF APPLICABLE',
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
    )

    labels = dmc.Group(
        id='chip-container',
        className='chip-container',
        style={'width': '100%'},
    )

    progress_bar = dmc.Progress(
        id='progress-bar',
        value=0,
        label='0%',
        color=styles.PRIMARY_COLOUR,
        radius='sm',
        size='xl',
    )

    stack = dmc.Stack(
        children=[
            modals.insert_modal_profile(),
            modals.insert_modal_statistics(),
            modals.insert_modal_quit(),
            drawer.insert_drawer_reference(),
            affixes.insert_affix_reference(),
        ],
        align='center',
        spacing='xl',
        pt='3%',
        pb=35,
    )

    spans = {
        'xl': 8,
        'lg': 10,
        'md': 12,
        'sm': 12,
        'xs': 12,
    }
    columns = [
        *header.insert_header(),
        dmc.Col(dmc.Center(title), **spans),
        dmc.Col(progress_bar,  **spans),
        dmc.Col(loading_paper, **spans),
        dmc.Col(labels, **spans),
        dmc.Col(dmc.Center(inputs.insert_select_comment()), **spans),
        dmc.Col(dmc.Center(buttons.insert_buttons_navigation()), **spans),
        dmc.Col(stack, **spans),
        dmc.Col(footer.insert_footer(), span=12),
    ]

    return columns


def get_finish_layout(reason: Literal['session_done', 'session_quit', 'no_tasks']):
    anchor_restart = dmc.Anchor(
        children=buttons.insert_button_restart(),
        href='/',
        refresh=True,
    )

    stack = dmc.Stack(
        children=[
            alerts.insert_alert_finish(reason=reason),
            anchor_restart,
        ],
        align='center',
        spacing='xl',
        pt='3%',
        pb=25,
    )

    spans = {
        'xl': 8,
        'lg': 10,
        'md': 12,
        'sm': 12,
        'xs': 12,
    }

    columns = [
        *header.insert_header(),
        dmc.Col(stack, **spans),
        dmc.Col(footer.insert_footer(), span=12),
    ]

    return columns
