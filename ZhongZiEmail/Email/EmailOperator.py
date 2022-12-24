import poplib
import smtplib
from Email import SentEmail
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


class EmailOperator:
    def __init__(self, user_message: list):
        self.username = user_message[0]
        self.passwd = user_message[1]
        self.pop3_server = user_message[2][0].split(":")[0]
        self.pop3_port = int(user_message[2][0].split(":")[1])
        self.smtp_server = user_message[2][1].split(":")[0]
        self.smtp_port = int(user_message[2][1].split(":")[1])

    def send(self, email: SentEmail):
        smtpobj = None
        try:
            smtpobj = smtplib.SMTP_SSL(self.smtp_server)
            smtpobj.connect(self.smtp_server, self.smtp_port)
            smtpobj.login(self.username, self.passwd)
            smtpobj.sendmail(email.sender, email.receiver, email.getMessage().as_string())
            return 0
        except smtplib.SMTPException:
            return -1
        finally:
            smtpobj.quit()
        pass

    def receive(self):
        pass

