import smtplib
import os
import time
import mimetypes
from pyfiglet import Figlet
from tqdm import tqdm
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase


def send_email(text=None, template=None):
    sender = "mt5.rport.sender@gmail.com"
    receiver = "anton.kurakin@gmail.com"
    password = "dbqxujnizlnjiaae"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        with open(template) as file:
            template = file.read()
    except IOError:
        template = None

    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = 'anton.kurakin@gmail.com'
        msg["Subject"] = "С Днем Рождения! Только сегодня скидка по промокоду до 90%!"

        if text:
            msg.attach(MIMEText(text))

        if template:
            msg.attach(MIMEText(template, "html"))

        print("Collecting...")
        for file in tqdm(os.listdir("txt")):
            time.sleep(0.4)
            filename = os.path.basename(file)
            ftype, encoding = mimetypes.guess_type(file)
            file_type, subtype = ftype.split("/")

            if file_type == "text":
                with open(f"txt/{file}") as f:
                    file = MIMEText(f.read())
            elif file_type == "image":
                with open(f"txt/{file}", "rb") as f:
                    file = MIMEImage(f.read(), subtype)
            elif file_type == "audio":
                with open(f"txt/{file}", "rb") as f:
                    file = MIMEAudio(f.read(), subtype)
            elif file_type == "application":
                with open(f"txt/{file}", "rb") as f:
                    file = MIMEApplication(f.read(), subtype)
            else:
                with open(f"txt/{file}", "rb") as f:
                    file = MIMEBase(file_type, subtype)
                    file.set_payload(f.read())
                    encoders.encode_base64(file)

            # with open(f"txt/{file}", "rb") as f:
            #     file = MIMEBase(file_type, subtype)
            #     file.set_payload(f.read())
            #     encoders.encode_base64(file)

            file.add_header('content-disposition', 'attachment', filename=filename)
            msg.attach(file)

        print("Sending...")
        server.sendmail(sender, receiver, msg.as_string())

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def main():
    font_text = Figlet(font="slant")
    print(font_text.renderText("SEND EMAIL"))
    text = input("Type your text or press enter: ")
    template = input("Type template name or press enter: ")
    print(send_email(text=text, template=template))


if __name__ == "__main__":
    main()