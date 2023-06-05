# dash
import dash_mantine_components as dmc

# local packages
from src import utils


def insert_alert_announcements():
    messages = utils.read_announcements_yaml()
    alerts = []
    for message in messages:
        alert = dmc.Alert(
            children=message['text'],
            title=message['title'],
            color=message['colour'],
            variant='outline',
        )
        alerts.append(alert)
    return alerts


def insert_alert_finish(reason):
    reason2message = {
        'session_done': 'Well done! If you feel like labelling more, click the button below.',
        'session_quit': 'Well done! You can return to the application at any time to contribute more.',
        'no_tasks': 'Well done! Looks like there are no more tasks in this language to be labelled by you.'
                    ' If you would like to contribute further, click the button below and try selecting a different'
                    ' language.'
    }
    message_default = 'Well done! If you want to start again, simply click the button below.'

    alert = dmc.Alert(
        children=reason2message.get(reason, message_default),
        title='Thank You for Your Contribution!',
        color='blue',
    )
    return alert
