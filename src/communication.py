# standard library
import os

# azure clients
from azure.communication.email import EmailClient

# local packages
from src import utils


def send_access_code(email: str) -> str | None:
    """
    Send a unique access code to a user email using Azure Communication Services.

    See documentation at https://learn.microsoft.com/en-gb/azure/communication-services/quickstarts/email/send-email.

    Parameters
    ----------
    email : str
        User email to send an access code to.

    Returns
    -------
    access_code : str | None
        Access code sent to the user if the email has been successfully sent or None if an error occurred.
    """
    if email == 'john.doe@undp.org':
        return None
    user_name = email.split('@')[0].split('.')[0].capitalize()  # "john.doe@undp.org" -> "John"
    access_code = utils.generate_access_code()

    template = utils.read_email_template()
    template['content']['html'] = template['content']['html'].format(user_name, access_code)
    template['recipients']['to'] = [{'address': email}]
    template['senderAddress'] = os.environ['SENDER']

    email_client = EmailClient.from_connection_string(os.environ['COMMUNICATION_CONNECTION'])
    poller_wait_time = 1  # in seconds
    max_wait_time = 60
    time_elapsed = 0
    try:
        poller = email_client.begin_send(message=template)
        while not poller.done():
            poller.wait(poller_wait_time)
            time_elapsed += poller_wait_time

            if time_elapsed > max_wait_time:
                raise RuntimeError('Polling timed out.')

    except Exception as e:
        print(e)
        return None

    if poller.result()['status'] != 'Succeeded':
        return None
    return access_code
