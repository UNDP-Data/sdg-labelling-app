# standard library
import os
import re
import json
import hashlib
from importlib import resources
from typing import get_args
from string import digits, ascii_letters
from random import choices

# local packages
from src import entities


def read_sdg_metadata() -> list[entities.SustainableDevelopmentGoal]:
    with resources.open_text('src.files', 'sdgs.json') as file:
        sdgs = json.load(file)
    sdgs = [entities.SustainableDevelopmentGoal(**sdg) for sdg in sdgs]
    return sdgs


def read_faq_markdown() -> str:
    with resources.open_text('src.files', 'faq.md') as file:
        content = file.read()
    return content


def read_email_template() -> dict:
    with resources.open_text('src.files', 'email.json') as file:
        template = json.load(file)
    return template


def get_language_mapping() -> dict:
    mapping = dict(sorted(zip(get_args(entities.LANGUAGE_ISO), get_args(entities.LANGUAGE_NAME)), key=lambda x: x[1]))
    return mapping


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
    pattern = r'^[a-z][\w.-]*@undp.org$'
    match = re.match(pattern=pattern, string=email, flags=re.IGNORECASE)
    is_valid = bool(match)
    return is_valid


def generate_access_code(length: int = 12) -> str:
    code = ''.join(choices(digits + ascii_letters, k=length))
    return code


def get_user_id(email: str) -> str:
    email = email.lower().strip()
    user_id = hashlib.md5(email.encode(encoding='utf-8')).hexdigest()
    return user_id


def get_user_label_and_comment(doc: dict, user_id: str):
    for annotation in doc.get('annotations', list()):
        if annotation['created_by'] == user_id:
            return annotation.get('labels'), annotation.get('comment')
    else:
        return None, None
