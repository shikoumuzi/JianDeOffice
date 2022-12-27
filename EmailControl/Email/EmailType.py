from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.header import Header
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.message import Message
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
        # self.message = MIMEText(content, 'plain', 'utf-8')
        main_body = MIMEText(content, 'plain', 'utf-8')
        self.message.attach(main_body)

    def setImage(self, image_path: str):
        if os.path.exists(image_path):
            image = MIMEImage(open(image_path, 'rb').read())
            image.add_header('Content-ID', '<image1>')
            # 现在要写add_header才不会导致乱码或者没有名字
            image.add_header("Content-Disposition", 'attachment', filename=os.path.split(image_path)[1])
            # 如果不加下边这行代码的话，会在收件方方面显示乱码的bin文件，下载之后也不能正常打开,这个地方也可以对文件重命名
            # image["Content-Disposition"] = 'attachment; filename=' + os.path.split(image_path)[1]
            self.message.attach(image)
            return 0
        return -1
        pass

    def setExcel(self, path: str) -> int:
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                xlsx = MIMEApplication(fp.read(), _subtype="'excel'")
            xlsx["Content-Type"] = 'application/octet-stream'
            xlsx.add_header("Content-Disposition", 'attachment', filename=os.path.split(path)[1])
            # xlsx["Content-Disposition"] = 'attachment; filename="' + os.path.split(path)[1] + '"'
            self.message.attach(xlsx)
            return 0
        return -1

    def setAccessory(self, path: str, subtype: str) -> int:
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                accessory = MIMEApplication(fp.read(), _subtype=subtype)
            accessory["Content-Type"] = 'application/octet-stream'
            # print(os.path.split(path)[1])
            accessory.add_header("Content-Disposition", 'attachment', filename=os.path.split(path)[1])
            self.message.attach(accessory)
            return 0
        return -1

    def getMessage(self) -> MIMEMultipart:
        return self.message


class ReceivedEmail:
    def __init__(self, eml_file: Message = None):
        """

        :param eml_file: if receive an email have file which is .eml file, this function will call itself again but
        put .eml file to be an arg into function
        """

        self.sender = ""
        self.receiver = ""
        self.content = []
        # 附件内容
        self.received_email = []  # eml 文件分析后的模块
        self.images = []
        self.excel = []
        self.word = []
        self.ppt = []
        self.music = []
        self.vedio = []
        self.pdf = []

    def getReceivedEmailfromAccessory(self) -> list:
        return self.received_email

    def getImages(self) -> list:
        return self.images

    def getMusic(self) -> list:
        return self.music

    def getVedio(self) -> list:
        return self.vedio

    def getPPT(self) -> list:
        return self.ppt

    def getWord(self) -> list:
        return self.word

    def getExcel(self) -> list:
        return self.excel

    def getPDF(self) -> list:
        return self.pdf
