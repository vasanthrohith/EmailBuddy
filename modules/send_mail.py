
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

mail_app_password=os.getenv("mail_app_password")



class SendMail_Notify:

    def __init__(self):
        pass
    def Send_Mail(self,mail_body,subject, sender_mail, rec_mail):
        print("--Send_Mail--")
        for dest in rec_mail:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender_mail, mail_app_password)
            subject=subject
            body=mail_body

            message = f"Subject: {subject}\n\n{body}"
            s.sendmail(sender_mail, dest, message)
            print(f"mail sent successfully to {dest}")
            s.quit()
