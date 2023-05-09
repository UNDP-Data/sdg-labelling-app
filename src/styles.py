
PRIMARY_COLOUR = '#1F5A95'


def get_sdg_style(sdg_id: int, is_selected: bool) -> dict:
    style_base = {
        'background-size': 'cover',
        'transition': '0.3s',
        'border': '2px solid transparent',
        'border-radius': '5px',
        'cursor': 'pointer',
    }
    if is_selected:
        style_extra = {
            'height': '10vh',
            'width': '10vh',
            'max-height': '10vh',
            'max-width': '10vh',
            'background-image': f'url("../assets/SDG_icons/color/en/sdg_{sdg_id}.png")',
            'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px',
        }
    else:
        style_extra = {
            'height': '9vh',
            'width': '9vh',
            'max-height': '9vh',
            'max-width': '9vh',
            'background-image': f'url("../assets/SDG_icons/black/en/sdg_{sdg_id}.png")',
        }
    style = style_base | style_extra
    return style
