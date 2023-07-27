# dash
import dash_mantine_components as dmc
from dash import dcc

# local packages
from src import utils
from src.ui import alerts, buttons, inputs, tables


def insert_modal_quit():
    title = dmc.Title(
        'Are you sure you want to quit?',
        order=2,
        ta='center'
    )

    text = dmc.Text(
        'Please note that once you quit this session, you will not be able to return to your progress.'
        ' However, your answers up to this point have been saved.',
        ta='center',
    )

    stack = dmc.Stack(
        children=[
            title,
            text,
            buttons.insert_button_quit_modal(),
        ],
        align='center',
        spacing='xl',
    )

    modal = dmc.Modal(
        id='modal-quit',
        centered=True,
        overlayBlur=10,
        transition='fade',
        children=stack,
    )
    return modal


def insert_modal_profile():
    title = dmc.Title(
        children='My Profile',
        order=2,
    )
    title_group = dmc.Group(
        children=[
            title,
            dmc.Badge(
              id='user-profile-id', 
              className='undp-chip undp-chip-blue', 
              size='xl'
            ),
        ],
        spacing='md',
    )
    modal = dmc.Modal(
        id={'type': 'modal', 'index': 'profile'},
        title=title_group,
        centered=True,
        size='xl',
        overlayBlur=10,
        transition='fade',
        children=inputs.insert_profile_settings(),
    )
    return modal


def insert_modal_statistics():
    title = dmc.Title(
        children='My Statistics',
        order=2,
    )
    modal = dmc.Modal(
        id={'type': 'modal', 'index': 'statistics'},
        title=title,
        centered=True,
        size='xl',
        overlayBlur=10,
        transition='fade',
        children='Coming soon.',
    )
    return modal


def insert_modal_announcements():
    title = dmc.Title(
        children='Announcements',
        order=2,
    )
    stack = dmc.Stack(
        children=alerts.insert_alert_announcements(),
        spacing='md',
    )
    modal = dmc.Modal(
        id={'type': 'modal', 'index': 'announcements'},
        title=title,
        centered=True,
        size='xl',
        overlayBlur=10,
        transition='fade',
        children=stack,
    )
    return modal


def insert_modal_leaderboard():
    title = dmc.Title(
        children='Leaderboard',
        order=2,
    )
    description = dmc.Text(
        children='If you want your name to appear on the leaderboard, log in to the application, open "My Profile",'
                 ' and turn on the switch next to "Display on Leaderboard".',
        size='sm',
    )
    stack = dmc.Stack(
        children=[
            description,
            tables.insert_table_leaderboard(),
        ],
    )
    modal = dmc.Modal(
        id={'type': 'modal', 'index': 'leaderboard'},
        title=title,
        centered=True,
        size='xl',
        overlayBlur=10,
        transition='fade',
        children=stack,
    )
    return modal


def insert_modal_faq():
    title = dmc.Title(
        children='Frequently Asked Questions',
        order=2,
    )
    modal = dmc.Modal(
        id={'type': 'modal', 'index': 'faq'},
        title=title,
        centered=True,
        size='xl',
        overlayBlur=10,
        transition='fade',
        children=dcc.Markdown(utils.read_faq_markdown()),
    )
    return modal
