# standard library
import os
from typing import Literal, get_args

# dash
import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify

# local packages
from src import styles, entities, utils


def get_sdg_item(sdg):
    list_targets = dmc.List([dmc.ListItem(target) for target in sdg.targets], spacing=10)
    item_control = dmc.AccordionControl(f'Goal {sdg.id}: {sdg.name}')
    item_panel = dmc.AccordionPanel(list_targets)
    item = dmc.AccordionItem(
        children=[item_control, item_panel],
        value=str(sdg.id),
    )
    return item


def get_sdg_drawer():
    sdgs = utils.read_sdg_metadata()
    items = [get_sdg_item(sdg) for sdg in sdgs]
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


def get_progress_rings():
    rings = list()
    for iso, name in zip(get_args(entities.LANGUAGE_ISO), get_args(entities.LANGUAGE_NAME)):
        ring = dmc.RingProgress(
            id={'type': 'ring', 'index': iso},
            label=dmc.Center(dmc.Text(iso.upper(), color=styles.PRIMARY_COLOUR)),
            size=80,
            thickness=10,
            roundCaps=False,
            sections=[{'value': 0, 'color': styles.PRIMARY_COLOUR}],
        )

        target = int(os.environ['PER_LANGUAGE_GOAL'])
        ring_with_tooltip = dmc.Tooltip(
            label=f'Progress in collecting {target:,} labelled examples for {name}. Updates every few seconds.',
            style={'cursor': 'pointer'},
            children=ring,
            withArrow=True,
            openDelay=1_000,
        )
        rings.append(ring_with_tooltip)
    return rings


def insert_user_stats(n_labels: int):
    text = dmc.Text('Your contribution', weight=100)
    badge = dmc.Badge(f'{n_labels} labels', color='red', variant='light')
    return [text, badge]


def get_header():
    group_user = dmc.Group(
        id='user-stats',
        children=None,
    )

    icon = DashIconify(
        icon='mdi:github',
        width=40,
        color='black',
    )

    anchor = dmc.Anchor(
        children=icon,
        href='https://github.com/UNDP-Data/sdg-labelling-app/issues',
        target='_blank',
    )

    button_faq = dmc.Button(
        'FAQ',
        id='faq-button',
        # size='lg',
        radius='md',
        color='red',
        variant='light',
        leftIcon=DashIconify(
            icon='wpf:faq',
            width=30,
        ),
    )

    title_group_right = dmc.Group(
        children=[group_user] + get_progress_rings() + [button_faq, get_faq_modal(), anchor],
        mr=0,
        ml='auto',
    )

    title = dmc.Title(
        'SDG Labelling Application',
        order=1,
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
    )

    badge = dmc.Badge('v0.2.1')

    divider = dmc.Divider(
        color=styles.PRIMARY_COLOUR,
        variant='solid',
    )

    title_group_left = dmc.Group(
        children=[title, badge],
    )

    title_row = dmc.Group(
        children=[title_group_left, title_group_right],
        w='100%',
    )

    header = dmc.Header(
        className='app-header',
        height=120,
        withBorder=True,
        children=[title_row, divider],
    )
    return header


def get_sdg_buttons(selected_sdg_ids: list[int] = None, language: entities.LANGUAGE_ISO = 'en'):
    sdg_button_list = []
    sdgs = utils.read_sdg_metadata()
    for sdg in sdgs:
        is_selected = selected_sdg_ids is not None and sdg.id in selected_sdg_ids
        button = html.Button(
            className='sdg-img-button',
            id={'type': 'sdg-button', 'index': sdg.id},
            n_clicks=int(is_selected),  # 1 if selected, 0 otherwise
            style=styles.get_sdg_style(sdg_id=sdg.id, is_selected=is_selected, language=language),
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

    tooltip_quit = dmc.Tooltip(
        children=button_quit,
        label='Quit the current session',
        position='top',
        offset=3,
        openDelay=500,
    )

    button_back = dmc.Button(
        'Back',
        id='back-button',
        n_clicks=0,
        size='md',
        radius='md',
        color=styles.PRIMARY_COLOUR,
        variant='light',
        disabled=True,
    )

    tooltip_back = dmc.Tooltip(
        children=button_back,
        label='Go back to the previous example',
        position='top',
        offset=3,
        openDelay=500,
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

    tooltip_next = dmc.Tooltip(
        children=button_next,
        label='Save and go to the next example',
        position='top',
        offset=3,
        openDelay=500,
    )

    buttons = dmc.Group(
        children=[tooltip_quit, tooltip_back, tooltip_next],
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
        'Select the number of texts you want to label',
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

    languages = sorted(zip(get_args(entities.LANGUAGE_ISO), get_args(entities.LANGUAGE_NAME)), key=lambda x: x[1])
    select_language = dmc.Select(
        id='language-input',
        label='Select a Language',
        description='If you are fluent in a language other than English, please select it.',
        data=[{'label': name, 'value': iso} for iso, name in languages],
        required=True,
        style={'width': '40%'},
        value='en',
    )

    input_email = dmc.TextInput(
        id='email-input',
        label='Enter Your Email',
        description='This must be your official UNDP email. It is only used for verification and will not be stored.',
        # value='john.doe@undp.org',  # uncomment while testing
        placeholder='john.doe@undp.org',
        style={'width': '40%'},
        required=True,
    )

    input_code = dmc.PasswordInput(
        id='code-input',
        label='Enter Your Access Code',
        description='This has been sent to your email. If you don\'t have a code or would like to get a new one,'
                    ' click the button on the right.',
        # value=os.environ['INVITATION_CODES'].split(',')[0],  # uncomment while testing
        placeholder='Invitation Code',
        style={'width': '40%'},
        required=True,
    )

    alert = dmc.Alert(
        'If you have not done so already, check out FAQ section before proceeding!'
        ' You can find it in the upper right corner.',
        title='FAQ Section Has Arrived!',
    )

    button_access = dmc.Button(
        'Get Access Code',
        id='email-button',
        size='md',
        radius='md',
        color='red',
        variant='light',
        rightIcon=DashIconify(icon='ic:baseline-email'),
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
            alert,
            title,
            text,
            slider,
            select_language,
            input_email,
            dmc.Group([input_code, button_access], position='center', grow=True, style={'width': '40%'}),
            button_start,
        ],
        align='center',
        spacing='xl',
        pt='3%',
    )
    return stack


def get_finish_layout(reason: Literal['session_done', 'session_quit', 'no_tasks']):
    if reason == 'session_done':
        message = 'Well done! If you feel like labelling more, click the button below.'
    elif reason == 'session_quit':
        message = 'Well done! You can return to the application at any time to contribute more.'
    elif reason == 'no_tasks':
        message = '''Well done! Looks like there are no more tasks in this language to be labelled by you. 
        If you would like to contribute further, click the button below and try selecting a different language.'''
    else:
        message = 'Well done! If you want to start again, simply click the button below.'

    alert = dmc.Alert(
        children=message,
        title='Thank You for Your Contribution!',
        color='blue',
    )

    button_restart = dmc.Button(
        'Label more',
        radius='md',
        size='lg',
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
        rightIcon=DashIconify(
            icon='ic:baseline-restart-alt',
            width=30,
        )
    )

    anchor_restart = dmc.Anchor(
        children=button_restart,
        href='/',
        refresh=True,
    )

    stack = dmc.Stack(
        children=[
            alert,
            anchor_restart,
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


def get_reference_affix():
    button_reference = dmc.Button(
        'Open SDG Reference',
        id='drawer-button',
        rightIcon=DashIconify(
            icon='mdi:chevron-double-right',
            width=30,
            color='white',
        ),
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
    )

    affix = dmc.Affix(
        children=button_reference,
        position={'bottom': 5, 'left': 5},
    )
    return affix


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

    input_comment = dmc.Select(
        id='comment',
        data=[
            'The text is irrelevant to SDGs.',
            'There is too little context to tell if the text is irrelevant to SDGs.',
            'The text is malformed, e.g., contains only URLs, references or numbers.',
            'The text is in a language other than the one I selected.',
        ],
        label='Add a comment (optional)',
        description='Select a value or start typing to add a custom comment (in English).',
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
        style={'width': '90%', 'margin': 'auto'}
    )

    stack = dmc.Stack(
        children=[
            title,
            progress_bar,
            loading_paper,
            labels,
            input_comment,
            get_button_container(),
            get_quit_modal(),
            get_sdg_drawer(),
            get_reference_affix(),
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
            'bottom': 5,
            'right': 5,
        }
    )
    return affix


def get_faq_modal():
    title = dmc.Title(
        'Frequently Asked Questions',
        order=2,
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
    )

    text = dcc.Markdown(utils.read_faq_markdown())

    modal = dmc.Modal(
        id='modal-faq',
        title=title,
        centered=True,
        size='xl',
        overlayBlur=10,
        transition='fade',
        children=text,
    )
    return modal


def get_notification_sending(email: str):
    message = f'We are sending your access code to {email}. This may take up to a minute.'
    notification = dmc.Notification(
        title='Sending..',
        id='notification-message',
        action='show',
        message=message,
        color='orange',
        loading=True,
        autoClose=False,
        disallowClose=True,
    )
    return notification


def get_notification_sent(email: str):
    message = f'We have just sent an email to {email} containing your personal access code.'\
              ' It may take a few minutes for the mail to arrive. Make sure to check your Spam folder.'
    notification = dmc.Notification(
        title='Email sent!',
        id='notification-message',
        action='update',
        message=message,
        icon=DashIconify(icon='akar-icons:circle-check'),
        color='green',
    )
    return notification


def get_notification_failed(email: str):
    message = f'An unexpected error occurred. We could not send an email to {email}.'\
              ' Please, double-check your email address and try again.'\
              ' If you still see this error, get in touch with us using the feedback button.'
    notification = dmc.Notification(
        title='Oops!',
        id='notification-message',
        action='update',
        message=message,
        icon=DashIconify(icon='fluent:mail-error-16-filled'),
        color='red',
    )
    return notification
