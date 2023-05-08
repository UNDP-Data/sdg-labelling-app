# standard library
import os
import re
import json
from importlib import resources
from collections import namedtuple


def read_sdg_metadata():
    with resources.open_text('src', 'sdgs.json') as file:
        sdgs = json.load(file)
    SDG = namedtuple('SustainableDevelopmentGoal', sdgs[0])
    sdgs = [SDG(**sdg) for sdg in sdgs]
    return sdgs


def validate_email(email: str) -> bool:
    """
    Check if the user email is a valid UNDP business address.

    Parameters
    ----------
    email : str
        User email.

    Returns
    -------
    is_valid : bool
        True if the email matches the pattern and False otherwise.

    Examples
    ________
    >>> validate_email('john.doe@undp.org')
    True
    >>> validate_email('John.Doe@undp.org')
    True
    >>> validate_email('john.van.der.doe@undp.org')
    True
    >>> validate_email('JOHN@UNDP.ORG')
    True
    >>> validate_email('john_doe@undp.org')
    False
    >>> validate_email('john.doe@gmail.com')
    False
    >>> validate_email('john.doe@undp.com')
    False
    """
    pattern = r'^[a-z][\w.]*@undp.org$'
    match = re.match(pattern=pattern, string=email, flags=re.IGNORECASE)
    is_valid = bool(match)
    return is_valid


def validate_code(code: str) -> bool:
    """
    Check if the invitation code is valid.

    Parameters
    ----------
    code : str
        Invitation code.

    Returns
    -------
    is_valid : bool
        True if the invitation code is valid and False otherwise.
    """
    valid_codes = set(os.environ['INVITATION_CODES'].split(','))
    is_valid = code in valid_codes
    return is_valid


def get_user_labels(doc: dict, email: str):
    for annotation in doc.get('annotations', list()):
        if annotation['email'] == email:
            return annotation['labels']
    else:
        return None
