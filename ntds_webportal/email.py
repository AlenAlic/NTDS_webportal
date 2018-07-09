from threading import Thread
from flask import current_app
from flask_mail import Message
from ntds_webportal import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body):
    if recipients == [None]:
        recipients = current_app.config['ADMINS'][0]
    sender = current_app.config['ADMINS'][0]
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # noinspection PyProtectedMember
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
