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
        color='black', # this is not working, changed it in the css file
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
        temporarily_unavailable = set()
        option = {
            'label': name if iso not in temporarily_unavailable else f'{name} (Temporarily Unavailable)',
            'value': iso,
            'disabled': iso in temporarily_unavailable,
        }
        data.append(option)
    select_language = dmc.Select(
        id='language-input',
        label='Select a Language',
        description='If you are fluent in a language other than English, please select it.',
        data=data,
        required=True,
        value='en',
        style={
            'width': '95%',
        },
    )
    return select_language


def insert_input_email():
    input_email = dmc.TextInput(
        id='email-input',
        label='Enter Your Email',
        description='This must be your official email, e.g., john.doe@undp.org, jane.doe@ec.europa.eu, '
                    ' jack.doe@who.int. It is only used for verification and will not be stored.',
        # value='john.doe@undp.org',  # comment out after testing
        placeholder='john.doe@undp.org',
        required=True,
        style={
            'width': '95%',
        },
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
        id='user-profile-leaderboard',
        size='md',
        radius='xl',
        color=styles.PRIMARY_COLOUR,
        label='Display on Leaderboard',
        checked=False
    )

    user_name = dmc.TextInput(
        id='user-profile-name',
        label='Enter Your Display Name',
        description='This name will appear on the leaderboard visible by everyone. If you don\'t want your username'
                    ' to be public, just turn off the switch above.',
        placeholder='Jane Doe',
        disabled=True,
    )

    team_name = dmc.TextInput(
        id='user-profile-team',
        label='Enter Your Team Name',
        description='Add a team name to associate yourself with other users.',
        placeholder='The Best Team',
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
