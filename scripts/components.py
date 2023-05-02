
import dash_mantine_components as dmc
from dash import html

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
    'red.7',
    'yellow.5',
    'green.7',
    'red.9',
    'orange.8',
    'blue.3',
    'yellow.4',
    'pink.8',
    'orange.6',
    'pink.5',
    'yellow.7',
    'yellow.6',
    'green.9',
    'blue.5',
    'lime.5',
    'blue.7',
    'blue.9'
]


def get_header():
    return dmc.Header(
        className='app-header',
        height=120,
        withBorder=True,
        children=[
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

    for sdg in SDG_LIST:
        chip = dmc.Chip(
            "SDG " + sdg['code'],
            className='chip',
            value=sdg['code'],
            variant='filled',
            radius='md',
            color=SDG_COLORS[int(sdg['code'])-1],
            checked=False,
        )

        tooltip = dmc.Tooltip(label=sdg['name'], children=[
                              chip], withArrow=True)
        chip_array.append(tooltip)

    return dmc.Container(
        id='chip-container',
        className='chip-container',
        children=chip_array,
    )


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
        'ASSIGN EACH PARAGRAPH TO THEIR MOST RELEVANT SDGs',
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
        dmc.Space(h=100),
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
                    dmc.Text("Your progress will be saved.",
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
