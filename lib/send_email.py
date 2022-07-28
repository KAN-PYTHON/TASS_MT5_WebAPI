# Скрипт отправки email
def send_email(user, pwd, recipient, subject, body):
    import smtplib
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP('smtp.gmail.com')
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")



user, pwd, recipient = 'kan.test1973@gmail.com', 'Kan373373', 'anton.kurakin@gmail.com'
subject = 'Drawdown limit'
body = 'Account has reached the drawdown limit'

send_email(user, pwd, recipient, subject, body)