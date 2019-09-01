from flask_mail import Message
from app import app, mail
from flask import render_template


def sendEmail(name, email, message):
    msg = Message(
        subject= 'New Message from - ' + name,
        sender=app.config['ADMINS'][0],
        recipients=[email]
    )

    # set the text and html body to a template render
    msg.body = render_template(
        'email/event_saved.txt', name=name, email=email, message=message
    )

    msg.html = render_template(
        'email/event_saved.html', name=name, email=email, message=message
    )

    mail.send(msg)
