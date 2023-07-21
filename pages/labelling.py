# web app
import dash
import dash_mantine_components as dmc

# local packages
import src

dash.register_page(__name__, path='/labelling')


def layout():
    title = dmc.Title(
        'Select SDGs Relevant for this paragraph if applicable',
        order=2,
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
        style={'fontSize': 'large', 'minHeight': '20vh', 'margin': '20px 0'},
    )

    loading_paper = dmc.LoadingOverlay(
        children=paper,
    )

    labels = dmc.Group(
        id='chip-container',
        className='chip-container',
        style={'width': '100%'},
    )

    progress_bar = dmc.Progress(
        id='progress-bar',
        value=0,
        label='0%',
        color='#D12800',
        radius='md',
        size='xl',
        style={'marginTop': '20px'},
    )

    stack = dmc.Stack(
        children=[
            src.ui.drawer.insert_drawer_reference(),
            src.ui.affixes.insert_affix_reference(),
        ],
        align='center',
        spacing='xl',
        pt='3%',
        pb=35,
    )

    spans = {
        'xl': 8,
        'lg': 10,
        'md': 12,
        'sm': 12,
        'xs': 12,
    }
    columns = [
        *src.ui.header.insert_header(),
        dmc.Col(dmc.Center(title), **spans),
        dmc.Col(progress_bar,  **spans),
        dmc.Col(loading_paper, **spans),
        dmc.Col(labels, **spans),
        dmc.Col(dmc.Center(src.ui.inputs.insert_select_comment()), **spans),
        dmc.Col(dmc.Center(src.ui.buttons.insert_buttons_navigation()), **spans),
        dmc.Col(stack, **spans),
        dmc.Col(src.ui.footer.insert_footer(), span=12),
    ]

    page = dmc.Grid(
        id='content',
        children=columns,
        justify='center',
        gutter='sm',
    )
    return page
