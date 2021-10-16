import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

class MailHandler():

    emailfrom = "kevin19930919@gmail.com"
    emailto = "kevin_tsai@leadtek.com.tw"
    username = "kevin19930919@gmail.com"
    password = "qjhuqjoqsvettkqj"
    
    @classmethod
    def mail_info(cls, contents):
        message = MIMEMultipart()
        message["From"] = cls.emailfrom
        message["To"] = cls.emailto
        message["Subject"] = "miner Warring"
        message.attach(MIMEText(contents))
        return message
    
    @classmethod
    def send_mail(cls,message):
        msg = cls.mail_info(message)
        
        try:
            with smtplib.SMTP_SSL(host="smtp.gmail.com", port="465") as server: 
                server.login(cls.username,cls.password)
                server.sendmail(cls.emailfrom, cls.emailto, msg.as_string())

        except Exception as e:
            print(e)