# dash
import dash_mantine_components as dmc


def insert_release_alerts():
    messages = {
        'FAQ Section Has Arrived!': 'We have added a FAQ section to answer common questions you might have about the'
                                    ' application and rationale behind it. If you have not done so already, check it'
                                    ' out before proceeding! You can find FAQ button in the upper right corner.',
        'Enhanced Security!': 'As we are scaling the application to hundreds of users, we have made changes to make'
                              ' everyone\'s experience more secure and private. Users can now only access the'
                              ' application with their personal access code. To request your code, enter you UNDP email'
                              ' and click on "Get Access Code". The code use receive is like a password. You can reuse '
                              ' use it to access the application multiple times. You do not need to request it every'
                              ' time. Once you receive the code, we recommend that you save it in your browser or'
                              ' password manager.'
    }
    alerts = []
    for title, text in messages.items():
        alert = dmc.Alert(
            children=text,
            title=dmc.Group([title, dmc.Badge('New')], spacing='sm'),
            color='blue',
            variant='outline',
            withCloseButton=True,
            style={'width': '50%'},
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
