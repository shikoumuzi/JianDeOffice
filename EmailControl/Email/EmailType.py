from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
import os


class SentEmail:
    def __init__(self):
        self.message = MIMEMultipart('mixed')
        self.sender = ""
        self.receiver = ""

    def setSender(self, sender: str):
        self.message['From'] = Header(sender, "utf-8")
        self.sender = sender

    def getSender(self) -> str:
        return self.sender

    def setReceiver(self, receiver: str):
        self.message['To'] = Header(receiver, "utf-8")
        self.receiver = receiver

    def getReceiver(self) -> str:
        return self.receiver

    def setSubject(self, subject: str):
        self.message['Subject'] = Header(subject, "utf-8")

    def setContent(self, content: str):
        self.message = MIMEText(content, 'plain', 'utf-8')
        # main_body = MIMEText(content, 'plain', 'utf-8')
        # self.message.attach(main_body)

    def setImage(self, image_path: str):
        if os.path.exists(image_path):
            image = MIMEImage(open(image_path, 'rb').read())
            image.add_header('Content-ID', '<image1>')
            # 如果不加下边这行代码的话，会在收件方方面显示乱码的bin文件，下载之后也不能正常打开,这个地方也可以对文件重命名
            image["Content-Disposition"] = 'attachment; filename="' + os.path.split(image_path)[1] + '"'
            self.message.attach(image)
            return 0
        return -1
        pass

    def setExcel(self, path: str) -> int:
        if os.path.exists(path):
            xlsx = MIMEText(open(path, 'rb').read(), "base64", "utf-8")
            xlsx["Content-Type"] = 'application/octet-stream'
            xlsx["Content-Disposition"] = 'attachment; filename="' + os.path.split(path)[1] + '"'
            self.message.attach(xlsx)
            return 0
        return -1

    def getMessage(self) -> MIMEMultipart:
        return self.message


class ReceivedEmail:
    def __init__(self):
        self.sender = ""
        self.receiver = ""
        self.content = ""
        pass
