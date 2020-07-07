import smtplib
import ssl
import os


def mail(reciever_email, message):
    port = 465

    password = "SpaceX@123"
    email = "gomoore705@gmail.com"
    context = ssl.create_default_context()

    server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
    server.login(email, password)

    sender_email = email

    server.sendmail(sender_email, reciever_email, message)
