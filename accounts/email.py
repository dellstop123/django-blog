import smtplib
import ssl
import os


def mail(reciever_email):
    port = 465

    password = os.environ.get('password')
    email = os.environ.get('email')
    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
    server.login(email, password)

    sender_email = email
    SUBJECT = "New Django Blog Developed by Guneet Singh !"
    TEXT = "Hi! Welcome to Django Blog"
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    server.sendmail(sender_email, reciever_email, message)
