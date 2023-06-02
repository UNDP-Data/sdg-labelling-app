# dash
import dash_mantine_components as dmc

# local packages
from src.ui import styles, buttons, modals, extras


def insert_header():
    title_group_right = dmc.Group(
        children=[
            extras.insert_user_stack(),
            *extras.insert_rings_progress(),
            buttons.insert_button_faq(),
            modals.insert_modal_faq(),
            extras.insert_anchor_github(),
        ],
        mr=0,
        ml='auto',
    )

    title = dmc.Title(
        'SDG Labelling Application',
        order=1,
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
    )

    subtitle = dmc.Text(
        'Make Your Contribution Towards a Safer And More Inclusive Use of Artificial Intelligence for'
        ' International Development',
        color=styles.PRIMARY_COLOUR,
        variant='gradient',
        size='sm',
        style={'overflow-wrap': 'break-word'},
    )

    title_stack = dmc.Stack(
        children=[title, subtitle],
        spacing='sm',
    )

    divider = dmc.Divider(
        color=styles.PRIMARY_COLOUR,
        variant='solid',
    )

    title_row = dmc.Group(
        children=[title_stack, title_group_right],
        w='100%',
    )

    header = dmc.Header(
        className='app-header',
        height=120,
        withBorder=True,
        children=[title_row, divider],
    )
    return header
