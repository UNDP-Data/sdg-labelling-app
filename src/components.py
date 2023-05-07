# dash
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

# local packages
from src import styles, utils


def get_header():
    nav_link = dmc.NavLink(
        label='Want to learn more about SDGs?',
        href='https://www.undp.org/sustainable-development-goals',
        target='_blank',
        icon=DashIconify(icon='bi:house-door-fill', height=16),
        active=True,
        variant='subtle',
        color='blue.8',
        style={'width': 'fit-content'},
        rightSection=DashIconify(icon='tabler-chevron-right')
    )

    title = dmc.Title(
        'SDG LABELLING PAGE',
        order=1,
        color='#1D3557',
        className='app-header-text',
    )

    header = dmc.Header(
        className='app-header',
        height=120,
        withBorder=True,
        children=[
            nav_link,
            title,
        ]
    )
    return header


def get_sdg_buttons(selected_sdg_ids: list[int] = None):
    sdg_button_list = []
    sdgs = utils.read_sdg_metadata()
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
    button_back = dmc.Button(
        'Back',
        id='back-button',
        n_clicks=0,
        size='md',
        radius='md',
        color='#50779A'
    )

    button_next = dmc.Button(
        'Next',
        id='next-button',
        n_clicks=0,
        size='md',
        radius='md',
        color='#50779A'
    )

    buttons = dmc.Group(
        children=[button_back, button_next],
        spacing='xl',
    )

    return buttons


def get_body_title():
    title = dmc.Title(
        'SELECT ONE OR MORE RELEVANT SDGs FOR EACH PARAGRAPH',
        order=2,
        color='#1D3557',
    )
    return title


def get_progress_bar():
    bar = dmc.Progress(
        id='progress-bar',
        value=0,
        label='0%',
        color='#50779A',
        radius='sm',
        size='xl',
        style={'width': '60%', 'margin': 'auto'}
    )
    return bar


def get_start_layout():
    divider = dmc.Divider(
        color='#1D3557',
        variant='solid'
    )

    title = dmc.Title(
        'LET\'S GET STARTED',
        order=2,
        color='#1D3557',
    )

    text = dmc.Text(
        'Select the number of paragraphs you want to label',
        style={'text-align': 'center'},
        color='#1D3557',
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
        color='cyan.9',
        marks=[
            {'value': 5, 'label': '5'},
            {'value': 100, 'label': '100'}
        ],
        value=30,
        style={'width': '45%'}
    )

    select_language = dmc.Select(
        id='language-input',
        label='Language',
        description='Select a language.',
        placeholder='Select a language',
        data=[
            {'label': 'en', 'value': 'en'},
            {'label': 'fr', 'value': 'fr'},
            {'label': 'es', 'value': 'es'},
            {'label': 'ru', 'value': 'ru'},
        ],
        required=True,
        style={'width': '15%'},
        value='en',
    )

    input_email = dmc.TextInput(
        id='email-input',
        label='Enter your email',
        placeholder='Enter your email',
        style={'width': '15%'},
        required=True,
    )

    button_start = dmc.Button(
        'Start',
        id='start-button',
        size='lg',
        radius='md',
        color='#50779A'
    )

    stack = dmc.Stack(
        children=[
            title,
            text,
            slider,
            select_language,
            input_email,
            button_start,
        ],
        align='center',
        spacing='xl',
        pt='5%',
    )
    return [get_header(), divider, stack]


def get_finish_layout():
    divider = dmc.Divider(
        color='#1D3557',
        variant='solid'
    )

    title = dmc.Title(
        'THANK YOU FOR YOUR PARTICIPATION!',
        order=2,
        color='#1D3557',
    )

    text = dmc.Text(
        'If you want to start again, click on the button below',
        color='#1D3557',
    )

    button_start_over = dmc.Button(
        'Start Over',
        id='start-over-button',
        size='md',
        radius='md',
        color='#50779A',
    )
    stack = dmc.Stack(
        children=[
            title,
            text,
            button_start_over,
        ],
        align='center',
        spacing='xl',
        pt='5%',
    )
    return [get_header(), divider, stack]


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
        color='red',
        variant='outline',
        id='quit-modal-button',
        size='lg'
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


def get_main_layout(paragraph: str):
    divider = dmc.Divider(
        color='#1D3557',
        variant='solid',
    )

    paper = dmc.Paper(
        paragraph,
        p='xl',
        id='paper',
        shadow='lg',
        radius='md',
        withBorder=True,
        className='paper'
    )

    labels = dmc.Container(
        id='chip-container',
        className='chip-container',
        children=get_sdg_buttons(),
    )

    button_quit = dmc.Button(
        'Quit',
        id='quit-button',
        size='lg',
        color='red',
        variant='subtle',
    )

    stack = dmc.Stack(
        children=[
            get_body_title(),
            paper,
            labels,
            get_button_container(),
            get_progress_bar(),
            button_quit,
            get_quit_modal(),
        ],
        align='center',
        spacing='xl',
        pt='5%',
    )

    return [get_header(), divider, stack]
