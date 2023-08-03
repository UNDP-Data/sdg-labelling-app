# local packages
from src import entities

PRIMARY_COLOUR = '#1F5A95'


def get_sdg_style(sdg_id: int, is_selected: bool, language: entities.LANGUAGE_ISO) -> dict:
    style_base = {
        'backgroundSize': 'cover',
        'transition': '0.3s',
        'border': '2px solid transparent',
        'borderRadius': '0px',
        'cursor': 'pointer',
    }
    if is_selected:
        style_extra = {
            'backgroundImage': f'url("../assets/icons/{language}/colour/sdg_{sdg_id}.png")',
            'height': '11vh',
            'width': '11vh',
            'boxShadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
        }
    else:
        style_extra = {
            'backgroundImage': f'url("../assets/icons/{language}/black/sdg_{sdg_id}.png")',
            'height': '10vh',
            'width': '10vh',
        }
    style = style_base | style_extra
    return style
