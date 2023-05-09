# standard library
import os
from typing import Literal

# dash
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

# local packages
from src import database, styles


def get_sdg__item(sdg):
    list_targets = dmc.List([dmc.ListItem(target) for target in sdg.targets], spacing=10)
    item_control = dmc.AccordionControl(f'Goal {sdg.id}: {sdg.name}')
    item_panel = dmc.AccordionPanel(list_targets)
    item = dmc.AccordionItem(
        children=[item_control, item_panel],
        value=str(sdg.id),
    )
    return item


def get_sdg_drawer():
    sdgs = database.read_sdg_metadata()
    items = [get_sdg__item(sdg) for sdg in sdgs]
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
            dmc.ScrollArea(accordion, h=500),  # this needs some adjustments
        ]
    )
    drawer = dmc.Drawer(
        title=dmc.Text('SDG Reference', weight=700),  # bold
        children=stack,
        id='drawer-reference',
        size='30%',
        padding='md',
        zIndex=10000,
    )
    return drawer


def get_header():
    icon = DashIconify(
        icon='mdi:github',
        width=40,
        color='black',
    )

    anchor = dmc.Anchor(
        children=icon,
        href='https://github.com/UNDP-Data/sdg-labelling-app/issues',
        target='_blank',
        mr=0,
        ml='auto',
    )

    title = dmc.Title(
        'SDG Labelling Application',
        order=1,
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
    )

    divider = dmc.Divider(
        color=styles.PRIMARY_COLOUR,
        variant='solid',
    )

    title_row = dmc.Group(
        children=[title, anchor],
        w='100%',
    )
    header = dmc.Header(
        className='app-header',
        height=120,
        withBorder=True,
        children=[title_row, divider],
    )
    return header


def get_sdg_buttons(selected_sdg_ids: list[int] = None):
    sdg_button_list = []
    sdgs = database.read_sdg_metadata()
    for sdg in sdgs:
        is_selected = selected_sdg_ids is not None and sdg.id in selected_sdg_ids
        button = html.Button(
            className='sdg-img-button',
            id={'type': 'sdg-button', 'index': sdg.id},
            n_clicks=int(is_selected),  # 1 if selected, 0 otherwise
            style=styles.get_sdg_style(sdg_id=sdg.id, is_selected=is_selected),
        )
        tooltip = dmc.Tooltip(
            label=sdg.name,
            style={'cursor': 'pointer'},
            children=button,
            withArrow=True
        )

        sdg_button_list.append(tooltip)

    return sdg_button_list


def get_button_container():
    button_quit = dmc.Button(
        'Quit',
        id='quit-button',
        size='lg',
        radius='md',
        color='red',
        variant='light',
        mr=0,
        ml='auto',
    )

    button_back = dmc.Button(
        'Back',
        id='back-button',
        n_clicks=0,
        size='md',
        radius='md',
        color=styles.PRIMARY_COLOUR,
        variant='light',
    )

    button_next = dmc.Button(
        'Next',
        id='next-button',
        n_clicks=0,
        size='md',
        radius='md',
        color=styles.PRIMARY_COLOUR,
        variant='light'
    )

    buttons = dmc.Group(
        children=[button_quit, button_back, button_next],
        spacing='xl',
    )

    return buttons


def get_start_layout():
    title = dmc.Title(
        'LET\'S GET STARTED',
        order=2,
        color=styles.PRIMARY_COLOUR,
        variant='gradient'
    )

    text = dmc.Text(
        'Select the number of paragraphs you want to label',
        style={'text-align': 'center'},
        color=styles.PRIMARY_COLOUR,
    )

    slider = dmc.Slider(
        className='slider',
        id='slider',
        min=5,
        max=100,
        step=5,
        size='lg',
        radius='md',
        showLabelOnHover=True,
        color='blue.8',
        marks=[
            {'value': 5, 'label': 'Just exploring'},
            {'value': 25, 'label': '25'},
            {'value': 50, 'label': '50'},
            {'value': 75, 'label': '75'},
            {'value': 100, 'label': 'I really want to contribute'}
        ],
        value=25,
        style={'width': '45%'}
    )

    select_language = dmc.Select(
        id='language-input',
        label='Select a Language',
        description='If you are fluent in a language other than English, please select it.',
        data=[
            {'label': 'English', 'value': 'en'},
            {'label': 'French', 'value': 'fr'},
            {'label': 'Russian', 'value': 'ru'},
            {'label': 'Spanish', 'value': 'es'},
        ],
        required=True,
        style={'width': '40%'},
        value='en',
    )

    input_email = dmc.TextInput(
        id='email-input',
        label='Enter Your Email',
        description='This must be your official UNDP email. It is only used for verification.',
        # value='john.doe@undp.org',  # uncomment while testing
        placeholder='john.doe@undp.org',
        style={'width': '40%'},
        required=True,
    )

    input_code = dmc.PasswordInput(
        id='code-input',
        label='Enter Your Invitation Code',
        description='This has been shared with you in the invitation email.',
        # value=os.environ['INVITATION_CODES'].split(',')[0],  # uncomment while testing
        placeholder='Invitation Code',
        style={'width': '40%'},
        required=True,
    )

    button_start = dmc.Button(
        'Start',
        id='start-button',
        size='lg',
        radius='md',
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
    )

    stack = dmc.Stack(
        children=[
            title,
            text,
            slider,
            select_language,
            input_email,
            input_code,
            button_start,
        ],
        align='center',
        spacing='xl',
        pt='3%',
    )
    return stack


def get_finish_layout(reason: Literal['session_done', 'session_quit', 'no_tasks']):
    title = dmc.Title(
        'Thank You for Your Contribution!',
        order=2,
        color=styles.PRIMARY_COLOUR,
    )

    if reason == 'session_done':
        message = 'Well done! If you feel like labelling more, simply restart the page in your browser to start over.'
    elif reason == 'session_quit':
        message = 'Well done! You can return to the application at any time to contribute more.'
    elif reason == 'no_tasks':
        message = '''Well done! Looks like there are no more tasks in this language to be labelled by you. 
        If you would like to contribute further, restart the page and try selecting a different language.'''
    else:
        message = 'Well done! If you want to start again, simply restart the page in your browser.'

    text = dmc.Text(
        message,
        color=styles.PRIMARY_COLOUR,
    )

    stack = dmc.Stack(
        children=[
            title,
            text,
        ],
        align='center',
        spacing='xl',
        pt='3%',
    )
    return stack


def get_quit_modal():
    title = dmc.Title(
        'Are you sure you want to quit?',
        order=2,
    )

    text = dmc.Text(
        'Please note that once you quit this session, you will not be able to return to your progress.'
        ' However, your answers up to this point have been saved.',
        ta='center',
    )

    button_quit = dmc.Button(
        'Quit',
        id='quit-modal-button',
        radius='md',
        size='lg',
        color='red',
        variant='outline',
    )

    stack = dmc.Stack(
        children=[
            title,
            text,
            button_quit,
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


def get_main_layout():
    button_info = dmc.Button(
        'Open SDG Reference',
        leftIcon=DashIconify(
            icon='material-symbols:quick-reference-outline',
            width=30,
            color='white',
        ),
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
        id='drawer-button',
    )

    title = dmc.Title(
        'SELECT ONE OR MORE SDGs RELEVANT FOR THIS PARAGRAPH',
        order=2,
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
    )

    paper = dmc.Paper(
        '',
        p='xl',
        id='paper',
        shadow='lg',
        radius='md',
        withBorder=True,
        ml='10%',
        mr='10%',
        style={'font-size': 'large', 'min-height': '20vh'}
    )

    labels = dmc.Container(
        id='chip-container',
        className='chip-container',
        children=get_sdg_buttons(),
    )

    input_comment = dmc.Select(
        id='comment',
        data=[
            'The text is irrelevant to SDGs.',
            'The text is malformed, e.g., contains only URLs, references or numbers.',
            'The text is in a language other than the one I selected.',
        ],
        label='Add a comment (optional)',
        description='Select a value or start typing to add a custom comment.',
        value=None,
        clearable=True,
        searchable=True,
        creatable=True,
        style={'max-width': '80%', 'min-width': '50%'},
    )

    progress_bar = dmc.Progress(
        id='progress-bar',
        value=0,
        label='0%',
        color=styles.PRIMARY_COLOUR,
        radius='sm',
        size='xl',
        style={'width': '60%', 'margin': 'auto'}
    )

    stack = dmc.Stack(
        children=[
            dmc.Group([title, button_info]),
            progress_bar,
            dmc.LoadingOverlay(paper),
            labels,
            input_comment,
            get_button_container(),
            get_quit_modal(),
            get_sdg_drawer(),
        ],
        align='center',
        spacing='xl',
        pt='3%',
    )

    return stack


def get_affix():
    text = dmc.Text(
        'Feedback',
        color=styles.PRIMARY_COLOUR,
        variant='gradient'
    )
    icon = dmc.ActionIcon(
        DashIconify(
            icon='ic:outline-feedback',
            width=50,
            color=styles.PRIMARY_COLOUR,
        ),
        size='lg',
        mb=10,
    )

    anchor = dmc.Anchor(
        children=dmc.Group([text, icon]),
        href=os.environ['MAILTO'],
        underline=False,
    )

    affix = dmc.Affix(
        children=anchor,
        position={
            'bottom': 20,
            'right': 20,
        }
    )
    return affix
