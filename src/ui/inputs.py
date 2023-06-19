# dash
import dash_mantine_components as dmc

# local packages
from src import utils
from src.ui import styles, buttons


def insert_slider_texts():
    slider_texts = dmc.Slider(
        className='slider',
        id='slider',
        min=5,
        max=100,
        step=5,
        size='md',
        radius='md',
        showLabelOnHover=True,
        color='blue.8',
        marks=[
            {'value': 5, 'label': '5'},
            {'value': 25, 'label': '25'},
            {'value': 50, 'label': '50'},
            {'value': 75, 'label': '75'},
            {'value': 100, 'label': '100'}
        ],
        value=25,
        style={'width': '95%'},  # avoid overflow for slider ends
    )
    return slider_texts


def insert_select_language():
    data = list()
    for iso, name in utils.get_language_mapping().items():
        coming_soon = {'ar', 'zh'}
        option = {
            'label': name if iso not in coming_soon else f'{name} (Temporarily Unavailable)',
            'value': iso,
            'disabled': iso in coming_soon,
        }
        data.append(option)
    select_language = dmc.Select(
        id='language-input',
        label='Select a Language',
        description='If you are fluent in a language other than English, please select it.',
        data=data,
        required=True,
        value='en',
        style={'width': '95%'},
    )
    return select_language


def insert_input_email():
    input_email = dmc.TextInput(
        id='email-input',
        label='Enter Your Email',
        description='This must be your official UNDP email. It is only used for verification and will not be stored.',
        # value='john.doe@undp.org',  # comment out after testing
        placeholder='john.doe@undp.org',
        required=True,
        style={'width': '95%'},
    )
    return input_email


def insert_input_passcode():
    input_passcode = dmc.PasswordInput(
        id='code-input',
        label='Enter Your Access Code',
        description='This has been sent to your email. If you don\'t have a code or would like to get a new one,'
                    ' click the button on the right.',
        # value='1234',  # comment out after testing
        placeholder='Type your code here',
        required=True,
        style={'width': '95%'},
    )
    return input_passcode


def insert_select_comment():
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
    return input_comment


def insert_profile_settings():
    profile_public = dmc.Switch(
        id='user-profile-public',
        size='md',
        radius='xl',
        color=styles.PRIMARY_COLOUR,
        label='Make my profile public',
        checked=False
    )

    user_name = dmc.TextInput(
        id='user-profile-display-name',
        label='Enter Your Display Name',
        description='This name will appear on the leaderboard visible by everyone. If you don\'t want your username'
                    ' to be public, just turn off the switch above.',
        placeholder='Jane Doe',
        disabled=True,
    )

    team_name = dmc.Select(
        id='user-profile-team-name',
        label='Enter Your Team Name',
        description='If you are part of team, select a team name below or create one!',
        placeholder='Jane Doe',
        data=[
            {'value': 'default', 'label': 'No Team'},
        ],
        searchable=True,
        creatable=True,
        disabled=True,
    )

    stack = dmc.Stack(
        children=[
            profile_public,
            user_name,
            team_name,
            buttons.insert_button_save_settings()
        ],
        spacing='xl',
    )
    return stack
