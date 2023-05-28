# dash
import dash_mantine_components as dmc


def insert_alert_faq():
    alert = dmc.Alert(
        'If you have not done so already, check out FAQ section before proceeding!'
        ' You can find it in the upper right corner.',
        title='FAQ Section Has Arrived!',
    )
    return alert


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
