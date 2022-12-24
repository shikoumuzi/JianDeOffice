from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from EmailOperator import EmailOperator


class EmailConnection:
    def __init__(self, passphrase: str):
        self.step = None
        self.username: str = ""
        self.passswd: str = ""
        key_pair = RSA.generate(4096)
        pem_format = 'PEM'
        self.base_key = passphrase
        self.public_key = key_pair.public_key().exportKey(pem_format, self.base_key)
        self.private_key = key_pair.exportKey(pem_format, self.base_key)
        self.encode_format = 'ISO-8859-1'
        self.user_name_path = "Config/usermessage.username"
        self.user_pwd_path = "Config/usermessage.password"
        open('../Config/public_key.pem', 'wb+').write(self.public_key)
        open('../Config/private_key.pem', 'wb+').write(self.private_key)
        self.server_address = {"qq": ("pop.qq.com:110", "smtp.qq.com:25"),
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
        with open(self.user_name_path, "w+") as user_name_file, \
                open(self.user_pwd_path, "wb+") as user_pwd_file:
            user_name_file.write(username + "\n")
            user_name_file.write(step)

            encrypted_passwd = PKCS1_OAEP.new(RSA.importKey(self.public_key, self.base_key)).encrypt(
                passwd.encode(self.encode_format))
            user_pwd_file.write(encrypted_passwd)

    def getUser(self):
        """
        use RSA, this is decoded function
        :return:
        """
        with open(self.user_name_path, "r") as user_name_file:
            username_file_content = user_name_file.readlines()
            self.username = username_file_content[0]
            if username_file_content[1] in self.server_address:
                self.step = self.server_address[username_file_content[1]]
            else:
                return 0

        password_from_file = b""
        with open(self.user_pwd_path, "rb") as user_pwd_file:
            password_from_file = user_pwd_file.read()
        cipher = PKCS1_OAEP.new(RSA.importKey(self.private_key, self.base_key))
        self.passswd = cipher.decrypt(password_from_file). \
            decode(self.encode_format)
        return 1

<<<<<<< HEAD:EmailControl/Email/EmailConnection.py
# connect = EmailConnection("ZhongZi")
# connect.setUser("qq", "muzi", "muzi")
# connect.getUser()
# connect.connection()
#
# oper = connect.connection()
=======

# connect = EmailConnection()
# connect.setUser("qq", "muzi", "muzi")
# connect.getUser()
# connect.connection()
>>>>>>> e22a4c7efefe896efa77e31c07895a11407f69ef:ZhongZiEmail/Email/EmailConnection.py
