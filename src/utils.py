# standard library
import re


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
