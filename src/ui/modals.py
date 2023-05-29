# dash
import dash_mantine_components as dmc
from dash import dcc

# local packages
from src import utils
from src.ui import styles, buttons


def insert_modal_faq():
    title = dmc.Title(
        'Frequently Asked Questions',
        order=2,
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
    )
    modal = dmc.Modal(
        id='modal-faq',
        title=title,
        centered=True,
        size='xl',
        overlayBlur=10,
        transition='fade',
        children=dcc.Markdown(utils.read_faq_markdown()),
    )
    return modal


def insert_modal_quit():
    title = dmc.Title(
        'Are you sure you want to quit?',
        order=2,
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
        id='modal',
        centered=True,
        overlayBlur=10,
        transition='fade',
        children=stack,
    )
    return modal
