from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients =recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
"""
send_async_email function that runs as a background thread would not have
worked, beacuse current_app is a context-awere variable that is tied to
the thread that is handling the client request.
The current_app._get_current_object() expression extracts the actual application
instance from inside the proxy object,
so that is what I passed to the thread as an argument.
"""
