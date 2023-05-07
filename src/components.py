# dash
import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify

SDG_LIST = [
    {'name': 'No poverty', 'code': '1'},
    {'name': 'Zero hunger', 'code': '2'},
    {'name': 'Good health and well-being', 'code': '3'},
    {'name': 'Quality education', 'code': '4'},
    {'name': 'Gender equality', 'code': '5'},
    {'name': 'Clean water and sanitation', 'code': '6'},
    {'name': 'Affordable and clean energy', 'code': '7'},
    {'name': 'Decent work and economic growth', 'code': '8'},
    {'name': 'Industry, innovation and infrastructure', 'code': '9'},
    {'name': 'Reduced inequalities', 'code': '10'},
    {'name': 'Sustainable cities and communities', 'code': '11'},
    {'name': 'Responsible consumption and production', 'code': '12'},
    {'name': 'Climate action', 'code': '13'},
    {'name': 'Life below water', 'code': '14'},
    {'name': 'Life on land', 'code': '15'},
    {'name': 'Peace, justice and strong institutions', 'code': '16'},
    {'name': 'Partnerships for the goals', 'code': '17'}
]


SDG_COLORS = [
    '#e5243b',
    '#DDA63A',
    '#4C9F38',
    '#C5192D',
    '#FF3A21',
    '#26BDE2',
    '#FCC30B',
    '#A21942',
    '#FD6925',
    '#DD1367',
    '#FD9D24',
    '#BF8B2E',
    '#3F7E44',
    '#0A97D9',
    '#56C02B',
    '#00689D',
    '#19486A'
]


def get_header():
    return dmc.Header(
        className='app-header',
        height=120,
        withBorder=True,
        children=[
            dmc.NavLink(
                label='Want to learn more about SDGs?',
                href='https://www.undp.org/sustainable-development-goals',
                target='_blank',
                icon = DashIconify(icon='bi:house-door-fill', height=16),
                active=True,
                variant='subtle',
                color='blue.8',
                style={
                    'width': 'fit-content',
                },
                rightSection=DashIconify(icon="tabler-chevron-right")
            ),
            dmc.Text(
                'SDG LABELLING PAGE',
                color="#1D3557",
                className='app-header-text',
                weight=700,
                size=40
            )
        ]
    )


def get_chips():
    chip_array = []
    i = 1

    for sdg in SDG_LIST:

        button = html.Button(
            className='sdg-img-button',
            id={'type': 'sdg-button', 'index': i},
            n_clicks=0,
            value=str(i-1),
            style={
                'height': '10vh',
                'width': '10vh',
                'max-height': '10vh',
                'max-width': '10vh',
                'background-image': 'url("../assets/SDG_icons/black/en/sdg_' + str(i) + '.png")',
                'background-size': 'cover',
                'transition': '0.3s',
                'border': '2px solid ' + '#000000',
                'border-radius': '5px',
                'cursor' : 'pointer'
            }
        )

        tooltip = dmc.Tooltip(label=sdg['name'],
                            style={'cursor' : 'pointer'},
                              children=[
            dcc.Store(
                id={'type': 'sdg-store', 'index': i},
                storage_type='memory',
                data={'clicked': False}),
            button],
            withArrow=True
        )
        chip_array.append(tooltip)
        i += 1

    return dmc.Container(
        id='chip-container',
        className='chip-container',
        children=chip_array,
    )


def get_blank_chip_array():
    chip_array = []
    i = 1

    for sdg in SDG_LIST:

        button = html.Button(
            className='sdg-img-button',
            id={'type': 'sdg-button', 'index': i},
            n_clicks=0,
            value=str(i-1),
            style={
                'height': '10vh',
                'width': '10vh',
                'max-height': '10vh',
                'max-width': '10vh',
                'background-image': 'url("../assets/SDG_icons/black/en/sdg_' + str(i) + '.png")',
                'background-size': 'cover',
                'transition': '0.3s',
                'border': '2px solid ' + '#000000',
                'border-radius': '5px',
                'cursor' : 'pointer'
            }
        )

        tooltip = dmc.Tooltip(label=sdg['name'],
                              style={'cursor' : 'pointer'},
                              children=[
            dcc.Store(
                id={'type': 'sdg-store', 'index': i},
                storage_type='memory',
                data={'clicked': False}),
            button],
            withArrow=True
        )
        chip_array.append(tooltip)
        i += 1

    return chip_array


def get_checked_chip_array(ids):
    chip_array = []
    i = 1

    for sdg in SDG_LIST:
        if i - 1 in ids:
            button = html.Button(
                className='sdg-img-button',
                id={'type': 'sdg-button', 'index': i},
                n_clicks=1,
                value=str(i-1),
                style={
                    'height': '11vh',
                    'width': '11vh',
                    'max-height': '11vh',
                    'max-width': '11vh',
                    'background-image': 'url("../assets/SDG_icons/color/en/sdg_'+str(i)+'.png")',
                    'background-size': 'cover',
                    'transition': '0.3s',
                    'border': '2px solid ' + SDG_COLORS[i-1],
                    'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
                    'border-radius': '5px',
                    'cursor' : 'pointer'
                }
            )

            tooltip = dmc.Tooltip(label=sdg['name'],
                                  style={'cursor' : 'pointer'},
                                  children=[
                dcc.Store(
                    id={'type': 'sdg-store', 'index': i},
                    storage_type='memory',
                    data={'clicked': True}),
                button],
                withArrow=True
            )
        else:
            button = html.Button(
                className='sdg-img-button',
                id={'type': 'sdg-button', 'index': i},
                n_clicks=0,
                value=str(i-1),
                style={
                    'height': '10vh',
                    'width': '10vh',
                    'max-height': '10vh',
                    'max-width': '10vh',
                    'background-image': 'url("../assets/SDG_icons/black/en/sdg_'+str(i)+'.png")',
                    'background-size': 'cover',
                    'transition': '0.3s',
                    'border': '2px solid ' + '#000000',
                    'border-radius': '5px',
                    'cursor' : 'pointer'
                    
                }
            )

            tooltip = dmc.Tooltip(label=sdg['name'],
                                  style={'cursor' : 'pointer'},
                                  children=[
                dcc.Store(
                    id={'type': 'sdg-store', 'index': i},
                    storage_type='memory',
                    data={'clicked': False}),
                button],
                withArrow=True
            )

        chip_array.append(tooltip)
        i += 1

    return chip_array


def get_button_container():
    return html.Div(
        className='button-container',
        children=[
            dmc.Button(
                'Back',
                id='back-button',
                size="md",
                radius='md',
                color='#50779A'
            ),
            dmc.Button(
                'Next',
                id='next-button',
                size="md",
                radius='md',
                color='#50779A'
            )
        ]
    )


def get_body_title():
    return dmc.Text(
        'SELECT ONE OR MORE RELEVANT SDGs FOR EACH PARAGRAPH',
        className='app-body-text',
        color="#1D3557",
        weight=700,
        size=25
    )


def get_progress_bar():
    return dmc.Progress(
        id='progress-bar',
        value=0,
        label="0%",
        color="#50779A",
        radius='sm',
        size='xl',
        style={'width': '60%', 'margin': 'auto'}
    )


def get_start_layout():
    return [
        get_header(),
        dmc.Divider(
            color="#1D3557",
            variant='solid'
        ),
        dmc.Space(h=50),
        dmc.Center(
            children=[
                html.Div(
                    className='app-body',
                    children=[
                        dmc.Text(
                            "LET'S GET STARTED",
                            color="#1D3557",
                            className='app-start-title',
                            weight=700,
                            size=40
                        ),
                        dmc.Text(
                            'Select the number of paragraphs you want to label',
                            style={
                                'text-align': 'center'
                            },
                            color="#1D3557",
                            weight=400,
                            size=20
                        ),
                        dmc.Space(h=50),
                        
                        dmc.Slider(
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
                        ),
                        dmc.Space(h=50),
                        dmc.Select(
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
                        ),
                        dmc.Space(h=20),
                        dmc.TextInput(
                            id='email-input',
                            label='Enter your email',
                            placeholder='Enter your email',
                            style={'width': '15%'},
                            required=True,
                        ),
                        dmc.Space(h=50),
                        dmc.Button(
                            'Start',
                            id='start-button',
                            size="lg",
                            radius='md',
                            color='#50779A'
                        )
                    ]
                )])
    ]


def get_finish_layout():
    return [
        get_header(),
        dmc.Divider(
            color="#1D3557",
            variant='solid'
        ),
        dmc.Space(h=100),
        dmc.Center(
            children=[
                html.Div(
                    className='app-body',
                    children=[
                        dmc.Text(
                            'THANK YOU FOR YOUR PARTICIPATION!',
                            color="#1D3557",
                            className='app-start-title',
                            weight=700,
                            size=40
                        ),
                        dmc.Text(
                            'If you want to start again, click on the button below',
                            color="#1D3557",
                            className='app-start-subtitle',
                            weight=200,
                            size=20
                        ),
                        dmc.Space(h=50),
                        dmc.Button(
                            'Start Over',
                            id='start-over-button',
                            size="md",
                            radius='md',
                            color='#50779A'
                        )
                    ]
                )])
    ]


def get_quit_modal():
    return dmc.Modal(
        id='modal',
        centered=True,
        overlayBlur=10,
        transition='fade',
        children=[
            html.Div(
                style={
                    'display': 'flex',
                    'flex-direction': 'column',
                    'align-items': 'center',
                },
                children=[
                    dmc.Text("Are you sure you want to quit?",
                             weight=700, size=20, color="#1D3557"),
                    dmc.Text("Please note that once you quit this session, you will not be able to return to your progress.  However, your answers up to this point have been saved.",
                             style={'text-align': 'center'},
                             weight=400, size=15, color="#1D3557"),
                    dmc.Space(h=20),
                    dmc.Group(
                        children=[
                            dmc.Button(
                                'Quit',
                                color="red",
                                variant="outline",
                                id='quit-modal-button',
                                size='lg'
                            )
                        ]
                    )
                ]
            )

        ]
    )


def get_main_layout(paragraph: str):
    return [html.Div(
        children=[
            get_header(),
            dmc.Divider(
                color="#1D3557",
                variant='solid'
            ),
            html.Div(
                className='app-body',
                children=[
                    get_body_title(),
                    dmc.Space(h=30),
                    dmc.Paper(
                        paragraph,
                        p="xl",
                        id='paper',
                        shadow="lg",
                        radius="md",
                        withBorder=True,
                        className='paper'
                    ),
                    dmc.Space(h=50),
                    get_chips(),
                    dmc.Space(h=50),
                    get_button_container()
                ]
            ),
            dmc.Space(h=40),
            get_progress_bar(),
            dmc.Space(h=40),
            dmc.Container(
                style={
                    'width': '90%',
                    'display': 'flex',
                    'flex-direction': 'row',
                    'justify-content': 'end'
                },
                children=[
                    dmc.Button("Quit",
                               id="quit-button",
                               size="lg",
                               color="red",
                               variant="subtle")
                ]
            ),
            get_quit_modal()
        ]

    )
    ]
