# dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def get_notification_sending(email: str):
    message = f'We are sending your access code to {email}. This may take up to a minute.'
    notification = dmc.Notification(
        title='Sending..',
        id='notification-message',
        action='show',
        message=message,
        color='orange',
        loading=True,
        autoClose=False,
        disallowClose=True,
    )
    return notification


def get_notification_sent(email: str):
    message = f'We have just sent an email to {email} containing your personal access code.'\
              ' It may take a few minutes for the mail to arrive. Make sure to check your Spam folder.'
    notification = dmc.Notification(
        title='Email sent!',
        id='notification-message',
        action='update',
        message=message,
        icon=DashIconify(icon='akar-icons:circle-check'),
        color='green',
    )
    return notification


def get_notification_failed(email: str):
    message = f'An unexpected error occurred. We could not send an email to {email}.'\
              ' Please, double-check your email address and try again.'\
              ' If you still see this error, get in touch with us using the feedback button.'
    notification = dmc.Notification(
        title='Oops!',
        id='notification-message',
        action='update',
        message=message,
        icon=DashIconify(icon='fluent:mail-error-16-filled'),
        color='red',
    )
    return notification
