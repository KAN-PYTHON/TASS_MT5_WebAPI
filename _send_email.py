import smtplib
from email.mime.text import MIMEText

# https://www.youtube.com/watch?v=RyoTETtvoFQ&t=151s

# password = "d4#Y4=fh-f"


def send_email_txt(receiver, subject, message):
    sender = "mt5.tassfx@gmail.com"
    password = "axyvxpilslxzvwrh"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.ehlo()
    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = subject
        server.sendmail(sender, receiver, msg.as_string())
    except Exception as _ex:
        return _ex
    return 0


def main():
    receiver = 'anton.kurakin@gmail.com'
    subject = 'Тебе письмо'
    message = 'Привет брат!'
    send_email_txt(receiver, subject, message)


if __name__ == "__main__":
    main()
