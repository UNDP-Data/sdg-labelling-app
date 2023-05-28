# dash
import dash_mantine_components as dmc

# local packages
from src import utils


def insert_slider_texts():
    slider_texts = dmc.Slider(
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
    return slider_texts


def insert_select_language():
    data = [{'label': name, 'value': iso} for iso, name in utils.get_language_mapping().items()]
    select_language = dmc.Select(
        id='language-input',
        label='Select a Language',
        description='If you are fluent in a language other than English, please select it.',
        data=data,
        required=True,
        style={'width': '40%'},
        value='en',
    )
    return select_language


def insert_input_email():
    input_email = dmc.TextInput(
        id='email-input',
        label='Enter Your Email',
        description='This must be your official UNDP email. It is only used for verification and will not be stored.',
        # value='john.doe@undp.org',  # comment out after testing
        placeholder='john.doe@undp.org',
        style={'width': '40%'},
        required=True,
    )
    return input_email


def insert_input_passcode():
    input_passcode = dmc.PasswordInput(
        id='code-input',
        label='Enter Your Access Code',
        description='This has been sent to your email. If you don\'t have a code or would like to get a new one,'
                    ' click the button on the right.',
        # value='1234',  # comment out after testing
        placeholder='Invitation Code',
        style={'width': '40%'},
        required=True,
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
