import poplib
import smtplib
from .EmailType import *
from email.parser import Parser
from email.message import Message
from email.header import decode_header
from email.utils import parseaddr


class EmailOperator:
    def __init__(self, user_message: list) -> None:
        self.username: str = user_message[0]
        self.passwd: str = user_message[1]
        self.pop3_server = user_message[2][0].split(":")[0]
        self.pop3_port = int(user_message[2][0].split(":")[1])
        self.smtp_server = user_message[2][1].split(":")[0]
        self.smtp_port = int(user_message[2][1].split(":")[1])

    def send(self, email: SentEmail) -> int:
        smtp = None
        try:
            smtp = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            # smtpobj.connect(self.smtp_server, self.smtp_port)
            smtp.ehlo()  # 向Gamil发送SMTP 'ehlo' 命令
            # smtp.starttls()
            smtp.login(self.username, self.passwd)
            smtp.sendmail(email.sender, email.receiver, email.getMessage().as_string())
            return 0
        except Exception as e:
            print(e.__str__())
            return -1
        finally:
            smtp.quit()
        pass

    def receive(self, email_file_num: int = 30) -> list:
        """

        :return: this is function will return an ovject which type is list include ReceivedEmail
        which include analized content
        """
        pop3 = poplib.POP3_SSL(self.pop3_server, self.pop3_port)
        pop3.user(self.username)
        pop3.pass_(self.passwd)
        resp, mails, octets = pop3.list()
        index = len(mails)
        # 获取最新三十封的邮件
        message_list = []
        for i in range(index + 1 - email_file_num, index + 1):
            resp, lines, octets = pop3.retr(i)  # 返回(状态信息，邮件，邮件尺寸)
            message_list.append(b'\r\n'.join(lines).decode('utf-8'))
        pop3.quit()

        received_email_list = []
        for i in range(email_file_num):
            received_email_list.append(ReceivedEmail(Parser.parsestr(message_list[i])))

        return received_email_list


