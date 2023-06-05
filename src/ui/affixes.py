# dash
import dash_mantine_components as dmc

# local packages
from src.ui import buttons


def insert_affix_reference():
    affix = dmc.Affix(
        children=buttons.insert_button_reference(),
        position={'bottom': 25, 'left': 5},
    )
    return affix
