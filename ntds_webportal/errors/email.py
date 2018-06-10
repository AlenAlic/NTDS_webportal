from flask import render_template, current_app
from ntds_webportal.email import send_email


def send_error_email(code, msg):
    send_email('xTDS WebPortal error: {}'.format(code),
               sender=current_app.config['ADMINS'][0],
               recipients=[current_app.config['ADMINS'][0]],
               text_body=render_template('email/error.txt', message=msg),
               html_body=render_template('email/error.html', message=msg))