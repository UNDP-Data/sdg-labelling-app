# standard library
import os
import re
import json
import hashlib
from importlib import resources

# local packages
from src import entities


def read_sdg_metadata() -> list[entities.SustainableDevelopmentGoal]:
    with resources.open_text('src', 'sdgs.json') as file:
        sdgs = json.load(file)
    sdgs = [entities.SustainableDevelopmentGoal(**sdg) for sdg in sdgs]
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


def hash_email(email: str) -> str:
    email = email.lower().strip()
    email_hashed = hashlib.md5(email.encode(encoding='utf-8')).hexdigest()
    return email_hashed


def get_user_label_and_comment(doc: dict, email: str):
    for annotation in doc.get('annotations', list()):
        if annotation['email'] == email:
            return annotation.get('labels'), annotation.get('comment')
    else:
        return None, None
