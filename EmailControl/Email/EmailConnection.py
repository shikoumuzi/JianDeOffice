from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from .EmailOperator import EmailOperator  # 导入包内的其他py文件需要加上  .  以表示在该包内
import os


class EmailConnection:
    def __init__(self, passphrase: str):
        self.step = None
        self.username: str = ""
        self.passswd: str = ""

        self.base_key = passphrase
        self.encode_format = 'ISO-8859-1'  # 测试后最稳妥的编码
        # 因为包管理器对相对路径而言几乎没有管辖权，所以需要根据本文件的绝对路径去求文件的相对路径
        self.folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # EmailControl的目录文件绝对路径
        self.user_name_path = os.path.join(self.folder, "Config/usermessage.username")
        self.user_pwd_path = os.path.join(self.folder, "Config/usermessage.password")
        self.server_address = {"qq": ("pop.qq.com:110", "smtp.qq.com:465"),
                               "163": ("pop.163.com:110", "smtp.163.com:25")}

    def connection(self):
        """
        this function is used to be connect to email serve
        :return: a EmailOperator object
        """
        print(self.step.__str__() + "\n" + self.username + self.passswd)
        return EmailOperator([self.username, self.passswd, self.step])

    def setUser(self, step: str, username: str, passwd: str):
        """
        use RSA, this is encryptied function
        :param step: server address
        :param username: username
        :param passwd: password
        :return:
        """
        key_pair = RSA.generate(4096)
        pem_format = 'PEM'
        public_key = key_pair.public_key().exportKey(pem_format, self.base_key)
        private_key = key_pair.exportKey(pem_format, self.base_key)

        with open(os.path.join(self.folder, 'Config/public_key.pem'), 'wb+') as tmp:
            tmp.write(public_key)
        with open(os.path.join(self.folder, 'Config/private_key.pem'), 'wb+') as tmp:
            tmp.write(private_key)

        with open(self.user_name_path, "w+") as user_name_file, \
                open(self.user_pwd_path, "wb+") as user_pwd_file:
            user_name_file.write(username + "\n")
            user_name_file.write(step)

            encrypted_passwd = PKCS1_OAEP.new(RSA.importKey(public_key, self.base_key)) \
                .encrypt(passwd.encode(self.encode_format))
            user_pwd_file.write(encrypted_passwd)

    def getUser(self):
        """
        use RSA, this is decoded function
        :return:
        """
        with open(self.user_name_path, "r") as user_name_file:
            username_file_content = user_name_file.readlines()
            self.username = username_file_content[0][:-1]  # python直接读入文件会将换行符读入
            if username_file_content[1] in self.server_address:
                self.step = self.server_address[username_file_content[1]]
            else:
                return 0

        private_key = b""
        with open(os.path.join(self.folder, 'Config/private_key.pem'), "rb") as fp:
            private_key = fp.read()
        password_from_file = b""
        with open(self.user_pwd_path, "rb") as user_pwd_file:
            password_from_file = user_pwd_file.read()

        cipher = PKCS1_OAEP.new(RSA.importKey(private_key, self.base_key))
        self.passswd = cipher.decrypt(password_from_file). \
            decode(self.encode_format)
        print(type(self.passswd))
        return 1

