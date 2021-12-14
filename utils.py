import re
import smtplib
import ssl

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PORT = 465
SMTP_SERVER = "smtp.gmail.com"

SENDER_EMAIL = "example@example.com"
RECEIVE_EMAIL = "example@example.com"
PASSWORD = "123456789"
MESSAGE = "BLA BLA BLA"


def check(email) -> bool:
    # pass the regular expression
    # and the string into the fullmatch() method
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def instant_email(sender_email, receiver_email, message):
    cont = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=cont) as server:
        password = input(f"Please enter password for your e-mail {sender_email}: ")
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
