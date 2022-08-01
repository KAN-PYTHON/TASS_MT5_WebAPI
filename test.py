def send_report_email(receiver, file_name):
    import os
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    try:
        sender = "mt5.rport.sender@gmail.com"
        password = "dbqxujnizlnjiaae"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.ehlo()
        server.login(sender, password)
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"
        quit()

    with open(file_name) as file:
        report_file = file.read()

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = "Bonus report - " + os.path.basename(file_name)
    message.attach(MIMEText(report_file, "html"))

    with open(file_name) as file:
        report_file = MIMEText(file.read())

    report_file.add_header('content-disposition', 'attachment', filename=os.path.basename(file_name))
    message.attach(report_file)

    try:
        server.sendmail(sender, receiver, message.as_string())
    except Exception as _ex:
        return f"{_ex}\nSend email error!"


send_report_email("anton.kurakin@gmail.com", "requirements.txt")
