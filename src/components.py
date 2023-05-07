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
        color=styles.PRIMARY_COLOUR,
        style={'width': 'fit-content'},
        rightSection=DashIconify(icon='tabler-chevron-right')
    )

    title = dmc.Title(
        'SDG Labelling Application',
        order=1,
        color=styles.PRIMARY_COLOUR,
    )

    divider = dmc.Divider(
        color=styles.PRIMARY_COLOUR,
        variant='solid'
    )

    header = dmc.Header(
        className='app-header',
        height=120,
        withBorder=True,
        children=[title, nav_link, divider]
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
        children=[button_back, button_next],
        spacing='xl',
    )

    return buttons


def get_body_title():
    title = dmc.Title(
        'SELECT ONE OR MORE RELEVANT SDGs FOR EACH PARAGRAPH',
        order=2,
        color=styles.PRIMARY_COLOUR,
    )
    return title


def get_progress_bar():
    bar = dmc.Progress(
        id='progress-bar',
        value=0,
        label='0%',
        color=styles.PRIMARY_COLOUR,
        radius='sm',
        size='xl',
        style={'width': '60%', 'margin': 'auto'}
    )
    return bar


def get_start_layout():
    title = dmc.Title(
        'LET\'S GET STARTED',
        order=2,
        color=styles.PRIMARY_COLOUR,
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
            {'value': 5, 'label': '5'},
            {'value': 100, 'label': '100'}
        ],
        value=30,
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
        placeholder='john.doe@undp.org',
        style={'width': '40%'},
        required=True,
    )

    input_code = dmc.TextInput(
        id='code-input',
        label='Enter Your Invitation Code',
        description='This has been shared with you in the invitation email.',
        # value='',
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
        variant='filled',
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
        pt='5%',
    )
    return stack


def get_finish_layout():
    title = dmc.Title(
        'THANK YOU FOR YOUR PARTICIPATION!',
        order=2,
        color=styles.PRIMARY_COLOUR,
    )

    text = dmc.Text(
        'If you want to start again, click on the button below',
        color=styles.PRIMARY_COLOUR,
    )

    button_start_over = dmc.Button(
        'Start Over',
        id='start-over-button',
        size='md',
        radius='md',
        color=styles.PRIMARY_COLOUR,
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


def get_main_layout(paragraph: str):
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
        radius='md',
        color='red',
        variant='light',
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

    return stack
