import smtplib
import ssl
import os


def mail(reciever_email, message):
    port = 465

    password = os.environ.get('password')
    email = os.environ.get('email')
    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
    server.login(email, password)

    sender_email = email

    server.sendmail(sender_email, reciever_email, message)
