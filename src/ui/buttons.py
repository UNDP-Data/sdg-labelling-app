# dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# local packages
from src import entities, utils
from src.ui import styles


def insert_button_faq():
    button = dmc.Button(
        'FAQ',
        id='faq-button',
        size='sm',
        radius='md',
        color='red',
        compact=True,
        variant='light',
        leftIcon=DashIconify(
            icon='wpf:faq',
            width=20,
        ),
    )
    tooltip = dmc.Tooltip(
        children=button,
        label='Open Frequently Asked Questions',
        position='top',
        offset=3,
        openDelay=500,
    )
    return tooltip


def insert_button_send():
    button = dmc.Button(
        'Get Access Code',
        id='email-button',
        size='md',
        color='red',
        variant='light',
        rightIcon=DashIconify(icon='ic:baseline-email'),
        style={
            'border-radius': '0px',
            'transition': 'all 0.3s ease-in-out',
        }
    )
    tooltip = dmc.Tooltip(
        children=button,
        label='Click to get your access code if you do not have one already',
        position='top',
        offset=3,
        openDelay=500,
    )
    return tooltip


def insert_button_login():
    button = dmc.Button(
        'LOG IN',
        id='button-log-in',
        size='lg',
        className='primary-button',
        rightIcon=DashIconify(
            icon='ep:arrow-up',
            rotate=1,
        ),
        radius='md',
    )
    tooltip = dmc.Tooltip(
        children=button,
        label='Click to log in',
        position='top',
        offset=3,
        openDelay=500,
    )
    return tooltip


def insert_button_start():
    button = dmc.Button(
        'START',
        id='start-button',
        className='primary-button',
        size='lg',
        radius='md',
        rightIcon=DashIconify(
            icon='ep:arrow-up',
            rotate=1,
            className='button-icon',
        ),
    )
    tooltip = dmc.Tooltip(
        children=button,
        label='Click to start labelling',
        position='top',
        offset=3,
        openDelay=500,
    )
    return tooltip


def insert_button_sdg(sdg: entities.SustainableDevelopmentGoal, is_selected: bool, language: entities.LANGUAGE_ISO):
    button = dmc.Button(
        id={'type': 'sdg-button', 'index': sdg.id},
        n_clicks=int(is_selected),  # 1 if selected, 0 otherwise
        style=styles.get_sdg_style(
            sdg_id=sdg.id, is_selected=is_selected, language=language),
    )
    tooltip = dmc.Tooltip(
        label=sdg.name,
        style={'cursor': 'pointer'},
        children=button,
        withArrow=True
    )
    return tooltip


def insert_buttons_sdg(selected_sdg_ids: list[int] = None, language: entities.LANGUAGE_ISO = 'en'):
    sdg_button_list = []
    sdgs = utils.read_sdg_metadata()
    for sdg in sdgs:
        is_selected = selected_sdg_ids is not None and sdg.id in selected_sdg_ids
        tooltip = insert_button_sdg(sdg, is_selected, language)
        sdg_button_list.append(tooltip)
    return sdg_button_list


def insert_button_quit():
    button = dmc.Button(
        'Quit',
        id='quit-button',
        className='secondary-button',
        size='lg',
        mr=0,
        ml='auto',
    )
    tooltip = dmc.Tooltip(
        children=button,
        label='Quit the current session',
        position='top',
        offset=3,
        openDelay=500,
    )
    return tooltip


def insert_button_back():
    button = dmc.Button(
        'Back',
        id='back-button',
        className='primary-button',
        n_clicks=0,
        size='lg',
        leftIcon=DashIconify(
            icon='ep:arrow-left',
        ),
        disabled=True,
    )
    tooltip = dmc.Tooltip(
        children=button,
        label='Go back to the previous example',
        position='top',
        offset=3,
        openDelay=500,
    )
    return tooltip


def insert_button_next():
    button = dmc.Button(
        'Next',
        id='next-button',
        className='primary-button',
        n_clicks=0,
        size='lg',
        rightIcon=DashIconify(
            icon='ep:arrow-up',
            rotate=1,
        )
    )
    tooltip = dmc.Tooltip(
        children=button,
        label='Save and go to the next example',
        position='top',
        offset=3,
        openDelay=500,
    )
    return tooltip


def insert_buttons_navigation():
    group_buttons = dmc.Group(
        children=[insert_button_back(),insert_button_quit(),
                  insert_button_next()],
        spacing='xl',
    )
    return group_buttons


def insert_button_restart():
    button = dmc.Button(
        'Label more',
        className='primary-button',
        size='lg',
        
    )
    tooltip = dmc.Tooltip(
        children=button,
        label='Click to restart the application and contribute more',
        position='top',
        offset=3,
        openDelay=500,
    )
    return tooltip


def insert_button_quit_modal():
    button = dmc.Button(
        'Quit',
        id='quit-modal-button',
        radius='md',
        size='lg',
    )
    tooltip = dmc.Tooltip(
        children=button,
        label='Click to quit your current session',
        position='top',
        offset=3,
        openDelay=500,
    )
    return tooltip


def insert_button_reference():
    button = dmc.Button(
        'Open SDG Reference',
        id='drawer-button',
        className='primary-button',
        size='lg',  
        rightIcon=DashIconify(
            icon='mdi:chevron-double-right',
            width=30,
            color='white',
        ),
    )
    tooltip = dmc.Tooltip(
        children=button,
        label='Click to open a quick SDG reference',
        position='top',
        offset=3,
        openDelay=500,
    )
    return tooltip


def insert_button_save_settings():
    button = dmc.Button(
        'Save',
        id='button-save-profile',
        size='lg',
        radius='md',
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
    )
    tooltip = dmc.Tooltip(
        children=dmc.LoadingOverlay(button),
        label='Click to save the settings',
        position='top',
        offset=3,
        openDelay=500,
    )
    return tooltip
