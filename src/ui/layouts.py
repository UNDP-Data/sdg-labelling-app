# standard library
from typing import Literal

# dash
import dash_mantine_components as dmc

# local packages
from src.ui import styles, alerts, buttons, inputs, modals, drawer, header, footer, affixes, accordions


def insert_login_elements():
    title = dmc.Title(
        'LOG IN',
        order=1,
        mt='5vh'
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
        'Let\'s get started',
        order=2,
    )

    text = dmc.Text(
        'Select the number of texts you want to label', className='label'
    )

    title_stack = dmc.Stack(
        children=[title, text],
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
